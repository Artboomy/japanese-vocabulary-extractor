#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard library imports
from pathlib import Path
import logging

# Local application imports
from main import ocr
from main import tokenizer
from main import csv
from main import args
from main import pdf


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    user_args = args.parse_arguments()
    provided_path = Path(user_args.input_path)
    output_file = None
    texts = []

    if user_args.type == "manga":
        texts.extend(texts_from_manga(provided_path, user_args.parent))
        output_folder = provided_path if user_args.parent else provided_path.parent
        output_file = output_folder / "vocab.csv"

    if user_args.type == "pdf":
        texts.extend(texts_from_pdf(provided_path))
        output_file = (
            provided_path.parent / "vocab.csv"
            if provided_path.is_file()
            else provided_path / "vocab.csv"
        )

    vocab = tokenizer.vocab_from_texts(texts)
    logging.info(f"Vocabulary: {vocab}")
    csv.save_vocab_to_csv(vocab, output_file)


def texts_from_manga(provided_path: Path, is_parent: bool) -> list:
    texts = []
    if not provided_path.is_dir():
        logging.error("Provided path is not a directory.")
        return
    texts.extend(ocr.text_from_folder(provided_path, user_args.parent))
    logging.debug(f"Texts: {texts}")
    return texts


def texts_from_pdf(provided_path: Path) -> list:
    pdfs = []
    texts = []
    if provided_path.is_dir():
        pdfs = provided_path.rglob("*.pdf")
    elif provided_path.is_file():
        pdfs = [provided_path]
    else:
        logging.error("Provided path is not a file or directory.")
        return
    for pdf_path in pdfs:
        texts.extend(pdf.text_from_pdf(pdf_path))
    logging.debug(f"Texts: {texts}")
    return texts


if __name__ == "__main__":
    main()
