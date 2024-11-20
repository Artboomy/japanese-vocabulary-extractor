#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import necessary modules from the package
from .ocr import text_from_folder
from .tokenizer import vocab_from_texts
from .main import main

# Define what is available when the package is imported
__all__ = ["text_from_folder", "vocab_from_texts", "main"]
