#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard library imports
import subprocess
import json
import logging
from pathlib import Path
import regex as re


def text_from_folder(path: str, is_parent: bool) -> str:
    run_mokuro(path, is_parent)
    return get_lines_from_mokuro_output(path, is_parent)


def run_mokuro(path: Path, is_parent: bool) -> None:
    try:
        command = ["mokuro", "--disable_confirmation=true"]
        if is_parent:
            command.append("--parent_dir=" + path.as_posix())
        else:
            command.append(path.as_posix())
        logging.info(f"Running mokuro with command: {command}")
        logging.info("This may take a while...")
        subprocess.run(command, text=True, check=True)
        logging.info("Mokuro finished running")
    except subprocess.CalledProcessError as e:
        logging.error("Mokuro failed to run.")


def get_lines_from_mokuro_output(path: Path, is_parent: bool) -> list:
    base_path = path if is_parent else path.parent
    ocr_result_path = base_path / "_ocr"
    json_files = ocr_result_path.rglob("*.json")
    all_lines = []
    for json_file in json_files:
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            for block in data.get("blocks", []):
                lines = block.get("lines", [])
                for line in lines:
                    # Sometimes the OCR hallucinates text where it shouldn't
                    # be and this results in very long strings of consecutive
                    # Kanji. This filters out most of these cases.
                    if max_consecutive_kanji(line) <= 10:
                        all_lines.append(line)

    return all_lines


def max_consecutive_kanji(s: str) -> int:
    # Regular expression to match Kanji characters
    kanji_regex = re.compile(r"\p{Han}")

    max_count = 0
    current_count = 0

    for char in s:
        if kanji_regex.match(char):
            current_count += 1
            max_count = max(max_count, current_count)
        else:
            current_count = 0

    return max_count
