#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard library imports
from pathlib import Path

# Third-party imports (install these with pip)
import pypdf


def texts_from_pdf(pdf_path: Path) -> list:
    pdf = pypdf.PdfReader(pdf_path.as_posix())
    pages = []
    for page in pdf.pages:
        pages.append(page.extract_text())
    return pages
