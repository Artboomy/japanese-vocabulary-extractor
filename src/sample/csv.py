#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Library Imports
import csv
import logging
from pathlib import Path
from tqdm import tqdm
import regex as re

# Local imports
from . import dictionary


def save_vocab_to_csv(vocab: set, output_file: Path):
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["word"])
        for word in vocab:
            writer.writerow([word])


def process_vocab_file(vocab_file: Path, add_english: bool, add_furigana: bool):
    line_count = count_lines(vocab_file)

    updated_rows = []
    with open(vocab_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        headers = next(reader)
        if add_english and "definition" not in headers:
            headers.append("definition")
        updated_rows.append(headers)

        for row in tqdm(
            reader,
            desc="Processing vocab file:",
            total=line_count - 1,
        ):
            word = row[0]

            # Get word information
            word_info = dictionary.get_word_info(word)
            if not word_info["is_real"]:
                logging.debug(f"Removing {word}")
                continue

            # Add English definition
            if add_english:
                row.append(word_info["definition"])

            # Add furigana
            if add_furigana and contains_kanji(word):
                row[0] = f"{word} ({word_info['kana']})"

            updated_rows.append(row)

    with open(vocab_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)


def count_lines(vocab_file: Path):
    with open(vocab_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        line_count = sum(1 for row in reader)
    return line_count


def contains_kanji(s: str) -> bool:
    return bool(re.search(r"\p{Han}", s))
