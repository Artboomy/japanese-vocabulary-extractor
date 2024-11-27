#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard library imports
import subprocess
import json
import logging
from pathlib import Path
import regex as re


def texts_from_manga_folder(path: Path, is_parent: bool) -> dict[str, list[str]]:
    run_mokuro(path, is_parent)
    return {path.name: get_lines_from_mokuro_output(path, is_parent)}


def texts_from_manga_chapters(path: str) -> dict[str, list[str]]:
    run_mokuro(path, is_parent=True)
    return get_lines_from_volumes(path)


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
        logging.info(
            "Mokuro finished running. Do not worry if it looks stuck for a second."
        )
    except subprocess.CalledProcessError as e:
        logging.error("Mokuro failed to run.")


def get_lines_from_volumes(path: Path) -> dict[str, list[str]]:
    chapters = {}
    # Get each individual folder containing json files
    json_folders = find_folders_with_json_files(path)
    for folder in json_folders:
        chapters[folder.name] = get_lines_from_json_folder(folder)
    return chapters


def find_folders_with_json_files(path: Path) -> set[Path]:
    json_files = path.rglob("*.json")
    folders = {
        json_file.parent
        for json_file in json_files
        if json_file.parent.parent == path / "_ocr"
    }
    return folders


def get_lines_from_json_folder(path: Path) -> list[str]:
    all_lines = []
    json_files = path.rglob("*.json")
    for json_file in json_files:
        all_lines.extend(process_json_file(json_file))
    return all_lines


def get_lines_from_mokuro_output(path: Path, is_parent: bool) -> list[str]:
    base_path = path if is_parent else path.parent
    ocr_result_path = base_path / "_ocr"
    json_files = ocr_result_path.rglob("*.json")
    all_lines = []
    for json_file in json_files:
        all_lines.extend(process_json_file(json_file))
    return all_lines


def process_json_file(json_file: Path) -> list[str]:
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
        return extract_lines_from_data(data)


def extract_lines_from_data(data: dict) -> list[str]:
    all_lines = []
    for block in data.get("blocks", []):
        lines = block.get("lines", [])
        for line in lines:
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
