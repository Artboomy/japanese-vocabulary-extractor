#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import necessary modules from the package
from .ocr import texts_from_manga_folder
from .tokenizer import vocab_from_texts
from .main import main
from .csv import save_vocab_to_csv, process_vocab_file
from .pdf import text_from_pdf
from .epub import texts_from_epub
from .args import parse_arguments
from .dictionary import get_word_info

# Define what is available when the package is imported
__all__ = [
    "texts_from_manga_folder",
    "vocab_from_texts",
    "main",
    "save_vocab_to_csv",
    "process_vocab_file",
    "text_from_pdf",
    "texts_from_epub",
    "parse_args",
    "lookup_definition",
]
