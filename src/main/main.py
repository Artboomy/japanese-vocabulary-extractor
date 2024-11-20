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


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    user_args = args.parse_arguments()

    provided_folder = Path(user_args.folder)

    texts = ocr.text_from_folder(provided_folder, user_args.parent)
    logging.debug(f"Texts: {texts}")
    vocab = tokenizer.vocab_from_texts(texts)
    logging.info(f"Vocabulary: {vocab}")

    output_folder = provided_folder if user_args.parent else provided_folder.parent
    output_file = output_folder / "vocab.csv"
    csv.save_vocab_to_csv(vocab, output_file)


if __name__ == "__main__":
    main()
