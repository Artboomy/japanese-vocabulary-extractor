#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Library Imports
import csv
import logging
from pathlib import Path
from tqdm import tqdm
import regex as re

# Local imports
from . import definition
from . import furigana


def save_vocab_to_csv(vocab: set, output_file: Path):
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["word"])
        for word in vocab:
            writer.writerow([word])


def add_english_to_vocab(vocab_file: Path, delay: float = 1.0):
    # First, count the number of lines in the file
    logging.info(f"Adding English definitions to {vocab_file}")
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
            desc="Loading definitions:",
            total=line_count - 1,
        ):
            word_definition = definition.lookup_definition(row[0])
            row.append(word_definition)
            if word_definition != "":
                updated_rows.append(row)

    with open(vocab_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)


def add_furigana(vocab_file: Path):
    contains_kanji_pattern = re.compile(r"[\p{Han}]+")

    # First, count the number of lines in the file
    logging.info(f"Adding furigana to {vocab_file}")
    with open(vocab_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        line_count = sum(1 for row in reader)

    updated_rows = []
    with open(vocab_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        headers = next(reader)
        if "furigana" not in headers:
            headers.append("furigana")
        updated_rows.append(headers)

        for row in tqdm(
            reader,
            desc="Loading furigana:",
            total=line_count - 1,
        ):
            word = row[0]
            if contains_kanji_pattern.match(word):
                print("HI")
                word = word + "(" + furigana.get_kana(word) + ")"
            row[0] = word
            print(word)
            updated_rows.append(row)

    with open(vocab_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)
