#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Library Imports
import requests
import logging


def lookup_definition(word: str) -> str:
    url = f"https://jisho.org/api/v1/search/words?keyword={word}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    try:
        if data["meta"]["status"] == 200:
            return ", ".join(data["data"][0]["senses"][0]["english_definitions"])
    except (IndexError, KeyError):
        logging.error(f"Could not find definition for {word}")
        return ""
