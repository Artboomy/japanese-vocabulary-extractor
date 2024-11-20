#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard library imports
import subprocess
import json
from pathlib import Path

def text_from_folder(path: str, is_parent: bool) -> str:
    run_mokuro(path, is_parent)
    return get_lines_from_mokuro_output(path, is_parent)

def run_mokuro(path: Path, is_parent: bool) -> None:
    try:
        command = ['mokuro', '--disable_confirmation=true']
        if is_parent:
            command.append('--parent_dir=' + path.as_posix())
        else:
            command.append(path.as_posix())
        print(f"Running command: {' '.join(command)}")
        print("This may take a while...")
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        print("Mokuro output:")
        print(result.stdout)
        if result.stderr:
            print("Mokuro errors:")
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error executing mokuro: {e}")

def get_lines_from_mokuro_output(path: Path, is_parent: bool) -> list:
    base_path = path if is_parent else path.parent
    ocr_result_path = base_path / "_ocr"
    json_files = ocr_result_path.rglob("*.json")
    all_lines = []
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for block in data.get('blocks', []):
                lines = block.get('lines', [])
                all_lines.extend(lines)
    return all_lines