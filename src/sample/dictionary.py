#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Library Imports
import logging
from jamdict import Jamdict


def get_jamdict_instance():
    jam = Jamdict()
    return jam


def get_word_info(word: str, jam) -> dict:
    result = jam.lookup(word)
    if len(result.entries) == 0:
        return {"definition": "", "kana": "", "is_real": False, "id": ""}
    definitions = result.entries[0]
    definition_text = ", ".join(sense.text() for sense in definitions.senses[:3])
    kana_text = definitions.kana_forms[0].text
    return {
        "definition": definition_text,
        "kana": kana_text,
        "is_real": True,
        "id": definitions.idseq,
    }
