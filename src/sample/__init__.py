#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import necessary modules from the package
from .ocr import (
    texts_from_manga_folder,
    texts_from_manga_chapters,
    run_mokuro,
    get_lines_from_volumes,
    find_folders_with_json_files,
    get_lines_from_json_folder,
    get_lines_from_mokuro_output,
    process_json_file,
    extract_lines_from_data,
)
from .tokenizer import vocab_from_texts
from .main import (
    main,
    texts_from_manga,
    texts_from_generic_file,
    generic_extract,
    get_files,
    get_output_file_path,
    configure_logging,
    check_invalid_options,
)
from .csv import save_vocab_to_csv, process_vocab_file, combine_csvs
from .pdf import texts_from_pdf
from .epub import texts_from_epub
from .args import parse_arguments
from .dictionary import get_word_info

# Define what is available when the package is imported
__all__ = [
    "texts_from_manga_folder",
    "texts_from_manga_chapters",
    "run_mokuro",
    "get_lines_from_volumes",
    "find_folders_with_json_files",
    "get_lines_from_json_folder",
    "get_lines_from_mokuro_output",
    "process_json_file",
    "extract_lines_from_data",
    "vocab_from_texts",
    "main",
    "texts_from_manga",
    "texts_from_generic_file",
    "generic_extract",
    "get_files",
    "get_output_file_path",
    "configure_logging",
    "check_invalid_options",
    "save_vocab_to_csv",
    "process_vocab_file",
    "combine_csvs",
    "texts_from_pdf",
    "texts_from_epub",
    "parse_arguments",
    "get_word_info",
]
