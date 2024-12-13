#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard library imports
from pathlib import Path
import logging
import colorlog
import sys
from tqdm.contrib.concurrent import thread_map
from multiprocessing import cpu_count

# Local application imports
from . import ocr
from . import tokenizer
from . import csv
from . import args
from . import pdf
from . import epub


def main():
    configure_logging()
    user_args = args.parse_arguments()
    check_invalid_options(user_args)

    provided_path = Path(user_args.input_path)
    logging.info(f"Extracting texts from {provided_path}...")

    extractors = {
        "manga": lambda: texts_from_manga(
            provided_path, user_args.parent, user_args.separate
        ),
        "pdf": lambda: texts_from_generic_file(
            provided_path, "pdf", pdf.texts_from_pdf
        ),
        "epub": lambda: texts_from_generic_file(
            provided_path, "epub", epub.texts_from_epub
        ),
        "txt": lambda: texts_from_generic_file(provided_path, "txt", generic_extract),
        "subtitle": lambda: texts_from_subtitles(provided_path),
        "generic": lambda: texts_from_generic_file(provided_path, "*", generic_extract),
    }

    try:
        results: dict[str, list[str]] = extractors[user_args.type.lower()]()
    except KeyError:
        logging.error("Invalid type provided.")
        sys.exit(1)

    # If user wishes not to separate, treat as one giant file
    if not user_args.separate:
        combined_values = []
        for value in results.values():
            combined_values.extend(value)
        results = {"all": combined_values}

    csvs = []
    for name, texts in results.items():
        logging.info(f"Getting vocabulary items from {name}...")
        vocab = tokenizer.vocab_from_texts(texts, user_args.freq_order)
        logging.info(f"Vocabulary from {name}: {', '.join(list(vocab)[:10])}, ...")
        output_file = get_output_file_path(provided_path, user_args.type, True, name)
        csv.save_vocab_to_csv(vocab, output_file)
        csvs.append(output_file)

    logging.info(
        f"Processing CSV(s) using dictionary (this might take a few minutes, do not worry if it looks stuck)..."
    )
    process_csvs(csvs, user_args)

    if user_args.separate:
        logging.info("Combining volumes into a single CSV file...")
        output = csv.combine_csvs(csvs)
        csvs.append(output)

    logging.info(
        f"Vocabulary saved into: {', '.join([csv.stem for csv in csvs])} in folder {csvs[0].parent.as_posix()}"
    )


def process_csvs(csvs, user_args):
    try:
        thread_map(
            lambda csv_file: csv.process_vocab_file(
                csv_file, user_args.add_english, user_args.furigana, user_args.id
            ),
            csvs,
            max_workers=cpu_count(),
        )
    except KeyboardInterrupt:
        logging.info("Process interrupted by user.")
        sys.exit(0)


def check_invalid_options(user_args):
    if user_args.parent and user_args.type != "manga":
        logging.error("Parent flag can only be used with manga.")
        sys.exit(1)

    if user_args.separate and user_args.type == "manga" and not user_args.parent:
        logging.error(
            "Separate can only be used with the parent attribute when processing manga."
        )
        sys.exit(1)

    if user_args.furigana and user_args.id:
        logging.error("Furigana and ID are incompatible.")
        sys.exit(1)


def texts_from_manga(
    provided_path: Path, is_parent: bool, separate_vols: bool
) -> dict[str, list[str]]:
    if not provided_path.is_dir():
        logging.error("Provided path is not a directory.")
        sys.exit(1)
    if separate_vols and is_parent:
        volumes = ocr.texts_from_manga_chapters(provided_path)
    else:
        volumes = ocr.texts_from_manga_folder(provided_path, is_parent)
    return volumes


def texts_from_generic_file(
    provided_path: Path, ext: str, extract_func
) -> dict[str, list[str]]:
    file_texts = {}
    files = get_files(provided_path, f"{ext}")
    for file in files:
        file_texts[file.stem] = extract_func(file)
    return file_texts


def texts_from_subtitles(
    provided_path: Path,
) -> dict[str, list[str]]:
    combined = texts_from_generic_file(provided_path, "ass", generic_extract)
    combined.update(texts_from_generic_file(provided_path, "srt", generic_extract))
    return combined


def generic_extract(provided_path) -> list[str]:
    return provided_path.read_text(encoding="utf-8").split()


def get_files(provided_path: Path, extension: str) -> list[Path]:
    if provided_path.is_dir():
        files = list(provided_path.rglob(f"*.{extension}"))
    elif provided_path.is_file():
        files = [provided_path]
    else:
        logging.error("Provided path is not a file or directory.")
        sys.exit(1)
    return [file for file in files if file.is_file()]


def get_output_file_path(
    provided_path: Path, type: str, is_parent: bool, add: str = ""
) -> Path:
    add = f"_{add}" if add else ""
    file_name = "vocab" + add + ".csv"
    if type == "manga":
        return (
            provided_path / file_name if is_parent else provided_path.parent / file_name
        )
    else:
        return (
            provided_path.parent / file_name
            if provided_path.is_file()
            else provided_path / file_name
        )


def configure_logging() -> None:
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s%(reset)s | \033[1m%(log_color)s%(levelname)s%(reset)s\033[0m | %(log_color)s%(name)s%(reset)s - \033[1m%(message)s\033[0m"
        )
    )
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)

    jamdict_logger = logging.getLogger("chirptext.leutile")
    jamdict_logger.setLevel(
        logging.WARNING
    )  # Set to WARNING to suppress INFO logs about config loads


if __name__ == "__main__":
    main()
