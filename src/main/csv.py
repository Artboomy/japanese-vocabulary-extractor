#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Library Imports
import csv
from pathlib import Path


def save_vocab_to_csv(vocab: set, output_file: Path):
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["word"])
        for word in vocab:
            writer.writerow([word])
