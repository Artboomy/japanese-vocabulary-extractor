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
    provided_path = Path(user_args.input_path)
    logging.info(f"Extracting texts from {provided_path}...")

    extractors = {
        "manga": lambda: texts_from_manga(provided_path, user_args.parent),
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
        texts = extractors[user_args.type]()
    except KeyError:
        logging.error("Invalid type provided.")
        exit(1)

    logging.debug(f"Texts: {texts[:50]}")

    output_file = get_output_file_path(provided_path, user_args.type, user_args.parent)

    logging.info(f"Getting vocabulary items from texts...")
    vocab = tokenizer.vocab_from_texts(texts)
    logging.info(f"Vocabulary: {vocab}")
    csv.save_vocab_to_csv(vocab, output_file)

    if user_args.add_english:
        csv.add_english_to_vocab(output_file)

    logging.info(f"Vocabulary saved to {output_file}")


def texts_from_manga(provided_path: Path, is_parent: bool) -> list[str]:
    if not provided_path.is_dir():
        logging.error("Provided path is not a directory.")
        exit(1)

    return ocr.text_from_folder(provided_path, is_parent)


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


def get_output_file_path(provided_path: Path, is_manga: bool, is_parent: bool) -> Path:
    if is_manga:
        return (
            provided_path / "vocab.csv"
            if is_parent
            else provided_path.parent / "vocab.csv"
        )
    else:
        return (
            provided_path.parent / "vocab.csv"
            if provided_path.is_file()
            else provided_path / "vocab.csv"
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
