#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard library imports
from pathlib import Path

import logging

# Local application imports
from . import ocr
from . import separator
from . import csv

def parse_arguments():
    """Parse command-line arguments."""
    import argparse
    parser = argparse.ArgumentParser(description="This script allows you to extract a vocabulary list from a folder of manga images.")
    parser.add_argument("--parent", action="store_true", help="Provided folder contains multiple volumes. Each folder will be treated as its own volume.")
    parser.add_argument("folder", type=str, help="Path to the folder.")
    return parser.parse_args()

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    args = parse_arguments()

    provided_folder = Path(args.folder)

    texts = ocr.text_from_folder(provided_folder, args.parent)
    logging.debug(f"Texts: {texts}") 
    vocab = separator.vocab_from_texts(texts)
    logging.info(f"Vocabulary: {vocab}")

    output_folder = provided_folder if args.parent else provided_folder.parent
    output_file = output_folder / "vocab.csv"
    csv.save_vocab_to_csv(vocab, output_file)
            
if __name__ == "__main__":
    main()