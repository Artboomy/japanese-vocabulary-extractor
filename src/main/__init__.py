#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import necessary modules from the package
from .ocr import text_from_folder
from .tokenizer import vocab_from_texts
from .main import main
from .csv import save_vocab_to_csv, add_english_to_vocab
from .pdf import text_from_pdf
from .epub import texts_from_epub
from .definition import lookup_definition

# Define what is available when the package is imported
__all__ = [
    "text_from_folder",
    "vocab_from_texts",
    "main",
    "save_vocab_to_csv",
    "add_english_to_vocab",
    "text_from_pdf",
    "texts_from_epub",
    "lookup_definition",
]
