#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard library imports
from pathlib import Path

# Third-party imports (install these with pip)
import ebooklib
from ebooklib import epub


def texts_from_epub(epub_path: Path) -> list:
    book = epub.read_epub(epub_path)
    texts = []
    for document in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        for item in document.get_body_content().decode("utf-8").split():
            texts.append(item)
    return texts
