#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard library imports
from pathlib import Path
import logging
import colorlog

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
            provided_path, user_args.parent, user_args.separate_vol
        ),
        "pdf": lambda: texts_from_generic_file(provided_path, "pdf", pdf.text_from_pdf),
        "epub": lambda: texts_from_generic_file(
            provided_path, "epub", epub.texts_from_epub
        ),
        "txt": lambda: texts_from_generic_file(provided_path, "txt", generic_extract),
        "subtitle": lambda: texts_from_generic_file(
            provided_path, "ass", generic_extract
        )
        + texts_from_generic_file(provided_path, "srt", generic_extract),
        "generic": lambda: texts_from_generic_file(provided_path, "*", generic_extract),
    }

    try:
        texts = extractors[user_args.type.lower()]()
    except KeyError:
        logging.error("Invalid type provided.")
        exit(1)

    # Handle saving one or multiple CSVs
    csvs = []
    if user_args.separate_vol and user_args.parent:
        chapters = texts[0]
        names = texts[1]
        for chapter, name in zip(chapters, names):
            logging.info(f"Getting vocabulary items from chatper {name}...")
            vocab = tokenizer.vocab_from_texts(chapter)
            logging.info(
                f"Vocabulary from chatper {name}: {", ".join(list(vocab)[:10])}, ..."
            )
            output_file = get_output_file_path(
                provided_path, user_args.type, True, name
            )
            csv.save_vocab_to_csv(vocab, output_file)
            csvs.append(output_file)
    else:
        logging.info(f"Getting vocabulary items from texts...")
        vocab = tokenizer.vocab_from_texts(texts)
        logging.info(f"Vocabulary: {", ".join(list(vocab)[:50])}, ...")
        output_file = get_output_file_path(
            provided_path, user_args.type, user_args.parent
        )
        csv.save_vocab_to_csv(vocab, output_file)
        csvs = [output_file]

    logging.info(f"Processing CSV(s) using dictionary...")
    for csv_file in csvs:
        csv.process_vocab_file(
            csv_file, user_args.add_english, user_args.furigana, user_args.id
        )

    if user_args.combine_vol:
        logging.info("Combining volumes into a single CSV file...")
        csv.combine_csvs(csvs)


def check_invalid_options(user_args):
    if user_args.separate_vol and not user_args.type == "manga":
        logging.error("Separate volumes can only be used with manga.")
        exit(1)

    if not user_args.separate_vol and user_args.combine_vol:
        logging.error("Combine volumes can only be used with separate volumes.")
        exit(1)

    if user_args.furigana and user_args.id:
        logging.error("Furigana and ID are incompatible.")
        exit(1)


def texts_from_manga(
    provided_path: Path, is_parent: bool, separate_vols: bool
):  # This might return a list of strings or a list of lists of strings depending on the "separate_vol" flag, definitely not optimal but it works for now
    if not provided_path.is_dir():
        logging.error("Provided path is not a directory.")
        exit(1)
    if separate_vols and is_parent:
        return ocr.texts_from_manga_chapters(provided_path)
    return ocr.texts_from_manga_folder(provided_path, is_parent)


def texts_from_generic_file(provided_path: Path, ext: str, extract_func) -> list[str]:
    texts = []
    files = get_files(provided_path, f"{ext}")
    for file in files:
        texts.extend(extract_func(file))
    return texts


def generic_extract(provided_path) -> list[str]:
    return provided_path.read_text().split()


def get_files(provided_path: Path, extension: str) -> list[Path]:
    if provided_path.is_dir():
        files = list(provided_path.rglob(f"*.{extension}"))
    elif provided_path.is_file():
        files = [provided_path]
    else:
        logging.error("Provided path is not a file or directory.")
        exit(1)
    return [file for file in files if file.is_file()]


def get_output_file_path(
    provided_path: Path, type: str, is_parent: bool, add: str = ""
) -> Path:
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


if __name__ == "__main__":
    main()
