#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Library Imports
import csv

from pathlib import Path
from tqdm import tqdm
from main import definition


def save_vocab_to_csv(vocab: set, output_file: Path):
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["word"])
        for word in vocab:
            writer.writerow([word])


def add_english_to_vocab(vocab_file: Path, delay: float = 1.0):
    # First, count the number of lines in the file
    with open(vocab_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        line_count = sum(1 for row in reader)

    updated_rows = []
    with open(vocab_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        headers = next(reader)
        if "definition" not in headers:
            headers.append("definition")
        updated_rows.append(headers)

        for row in tqdm(
            reader,
            desc="Loading definitions, this may take a while",
            total=line_count - 1,
        ):
            definition = definition.lookup_definition(row[0])
            row.append(definition)
            updated_rows.append(row)

    with open(vocab_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)
