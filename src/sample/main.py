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
    output_file = None
    texts = []

    match user_args.type:
        case "manga":
            texts = texts_from_manga(provided_path, user_args.parent)
        case "pdf":
            texts = texts_from_pdf(provided_path)
        case "epub":
            texts = texts_from_epub(provided_path)
        case "text":
            texts = texts_from_text_file(provided_path)
        case _:
            logging.error("Invalid type provided.")
            exit(1)

    logging.debug(f"Texts: {texts[:50]}")

    output_file = get_output_file_path(provided_path, user_args.type, user_args.parent)

    vocab = tokenizer.vocab_from_texts(texts)
    logging.info(f"Vocabulary: {vocab}")
    csv.save_vocab_to_csv(vocab, output_file)

    if user_args.add_english:
        csv.add_english_to_vocab(output_file)


def texts_from_manga(provided_path: Path, is_parent: bool) -> list:
    texts = []
    if not provided_path.is_dir():
        logging.error("Provided path is not a directory.")
        return
    texts.extend(ocr.text_from_folder(provided_path, is_parent))
    return texts


def texts_from_pdf(provided_path: Path) -> list:
    texts = []
    pdfs = get_files(provided_path, "pdf")
    for pdf_path in pdfs:
        texts.extend(pdf.text_from_pdf(pdf_path))
    return texts


def texts_from_epub(provided_path: Path) -> list:
    texts = []
    epubs = get_files(provided_path, "epub")
    for epub_path in epubs:
        texts.extend(epub.texts_from_epub(epub_path))
    return texts


def texts_from_text_file(provided_path: Path) -> list:
    files = get_files(provided_path, "txt")
    texts = []
    for file in files:
        texts.extend(file.read_text().split())
    return texts


def get_files(provided_path: Path, extension: str) -> list:
    files = []
    if provided_path.is_dir():
        files = provided_path.rglob(f"*.{extension}", case_sensitive=False)
    elif provided_path.is_file():
        files = [provided_path]
    else:
        logging.error("Provided path is not a file or directory.")
        exit(1)
    return files


def get_output_file_path(
    provided_path: Path, type: str, is_parent: bool = False
) -> Path:
    if type == "manga":
        return (
            provided_path.parent / "vocab.csv"
            if provided_path.is_file()
            else provided_path / "vocab.csv"
        )
    else:  # pdf or epub
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
