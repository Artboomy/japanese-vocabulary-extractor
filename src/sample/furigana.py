#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Library Imports


# Third-party imports (install these with pip)
import MeCab


def get_kana(word: str) -> str:
    mecab = MeCab.Tagger()
    parsed = mecab.parse(word)
    words = parsed.split("\n")
    for word in words:
        word_info = word.split("\t")
        if word == "EOS" or word == "" or len(word_info) < 2:
            continue
        kana = word_info[1]
    return kata2hira(kana)


# Turns katakana into hiragana, because MeCab provides the readings in katakana
def kata2hira(text: str) -> str:
    return "".join(
        chr(ord(char) - 0x60) if "ァ" <= char <= "ン" else char for char in text
    )
