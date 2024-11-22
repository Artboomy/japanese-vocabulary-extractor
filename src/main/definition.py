#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Library Imports
import requests
import logging
from jamdict import Jamdict


def lookup_definition(word: str) -> str:
    jam = Jamdict()
    result = jam.lookup(word)
    if len(result.entries) == 0:
        logging.error(f"Could not find definition for {word}")
        return ""
    definitions = result.entries[0]
    return ", ".join(sense.text() for sense in definitions.senses[:3])
