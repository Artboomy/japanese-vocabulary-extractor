#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard library imports
from pathlib import Path
import csv

# Local application imports
import ocr
import separator

def parse_arguments():
    """Parse command-line arguments."""
    import argparse
    parser = argparse.ArgumentParser(description="A brief script description.")
    parser.add_argument("--parent", action="store_true", help="Provided folder contains multiple volumes. Each folder will be treated as its own volume.")
    parser.add_argument("folder", type=str, help="Path to the folder.")
    return parser.parse_args()

def main():
    args = parse_arguments()

    provided_folder = Path(args.folder)

    texts = ocr.text_from_folder(provided_folder, args.parent)
    vocab = separator.vocab_from_texts(texts)
    print(f"Vocabulary: {vocab}")

    output_folder = provided_folder.parent
    if args.parent:
        output_folder = provided_folder
    output_file = output_folder / "vocab.csv"
    save_vocab_to_csv(vocab, output_file)
    
def save_vocab_to_csv(vocab: set, output_file: Path):
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["word"])
        for word in vocab:
            writer.writerow([word])
        
if __name__ == "__main__":
    main()
