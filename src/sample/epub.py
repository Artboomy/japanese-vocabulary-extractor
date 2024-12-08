#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard library imports
from pathlib import Path
import logging

# Third-party imports (install these with pip)
import ebooklib
from ebooklib import epub


def texts_from_epub(epub_path: Path) -> list:
    book = epub.read_epub(epub_path)
    texts = []
    for document in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        try:  # This try catch block skips documents that cause an exception because they apparently lack a body element. I believe this shouldn't be a problem because these documents shouldn't contain any text anyway.
            body_content = document.get_body_content()
            if body_content:
                for item in body_content.decode("utf-8").split():
                    texts.append(item)
        except TypeError:
            logging.warning("Found a document without a body tag, skipping.")
            continue
    return texts
