#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Library Imports
import csv
import logging
from pathlib import Path
import regex as re

# Local imports
from . import dictionary


def save_vocab_to_csv(vocab: list, output_file: Path):
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["word"])
        for word in vocab:
            writer.writerow([word])


def process_vocab_file(
    vocab_file: Path, add_english: bool, add_furigana: bool, id: bool
):
    jamdict = dictionary.get_jamdict_instance()

    updated_rows = []
    with open(vocab_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        headers = next(reader)
        if add_english:
            headers.append("definition")
        updated_rows.append(headers)

        for row in reader:
            word = row[0]
            word_info = dictionary.get_word_info(word, jamdict)

            # I currently decided one-letter kana words are not worth keeping in
            # because the definitions fetched for them are absolutely useless. This could
            # and should definitely be changed but I'm not really sure how to do it.
            one_character_kana = re.match(r"^\p{Hiragana}$|^\p{Katakana}$", word)
            if not word_info["is_real"] or (one_character_kana and add_english):
                logging.debug(f"Removing {word}")
                continue

            # Add English definition
            if add_english:
                row.append(word_info["definition"])

            # Add furigana
            if add_furigana and re.search(r"\p{Han}", word):
                row[0] = f"{word} ({word_info['kana']})"

            # Replace with ID if desired
            if id:
                row[0] = word_info["id"]

            updated_rows.append(row)

    with open(vocab_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)


def combine_csvs(csv_files: list[Path]) -> Path:
    new_rows = []

    # Add header
    with open(csv_files[0], "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)
        new_rows.append(header)

    # Sort csv files by file name
    csv_files.sort(key=lambda x: x.stem)

    # Add chapters
    for csv_file in csv_files:
        with open(csv_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            new_rows.append(["#" + csv_file.stem.replace("vocab_", "")])
            new_rows.extend(list(reader)[1:])

    # Remove all duplicates while preserving order
    known_words = set()
    i = 0
    while i < len(new_rows):
        if new_rows[i][0] in known_words:
            new_rows.pop(i)
            i -= 1
        else:
            known_words.add(new_rows[i][0])
        i += 1

    # Remove all empty chapters (chapters followed immediately by another chapter)
    i = 0
    while i < len(new_rows) - 1:
        if new_rows[i][0].startswith("#") and new_rows[i + 1][0].startswith("#"):
            new_rows.pop(i)
            i -= 1
        i += 1
    if new_rows[-1][0].startswith("#"):
        new_rows.pop(-1)

    # Write file
    with open(
        csv_files[0].parent / "vocab_combined.csv", "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerows(new_rows)

    return csv_files[0].parent / "vocab_combined.csv"
