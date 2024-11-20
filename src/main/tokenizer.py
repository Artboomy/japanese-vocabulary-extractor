#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard library imports
import regex as re
import logging

# Third-party imports (install these with pip)
import nagisa

def vocab_from_texts(texts: list) -> set:
    vocab = set()
    hiragana_katakana_kanji_pattern = re.compile(r'^\p{IsHiragana}|\p{IsKatakana}|\p{IsHan}+$')

    for text in texts:
        words = nagisa.tagging(text).words
        logging.debug(f"Words: {words}")
        for word in words:
            if hiragana_katakana_kanji_pattern.match(word):
                vocab.add(word)
        
    return vocab
