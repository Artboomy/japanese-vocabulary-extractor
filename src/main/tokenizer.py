#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard library imports
import regex as re

# Third-party imports (install these with pip)
import MeCab


def vocab_from_texts(texts: list) -> set:
    vocab = set()
    mecab = MeCab.Tagger()

    hiragana_katakana_kanji_pattern = re.compile(
        r"[\p{IsHiragana}\p{IsKatakana}\p{IsHan}]+"
    )
    katakana_only_pattern = re.compile(r"[\p{IsKatakana}]+")

    for text in texts:
        parsed = mecab.parse(text)
        words = parsed.split("\n")
        for word in words:
            if word == "EOS" or word == "":
                continue
            word_info = word.split("\t")
            if len(word_info) > 0:
                # For some reason the 4th element contains the english translation
                # for katakana-only words, so we differentiate between katakana-only
                # words and other words
                base_form = (
                    word_info[0]
                    if katakana_only_pattern.match(word_info[0])
                    else word_info[3]
                )
                # Sometimes the base form is followed by a hyphen and more text
                base_form = base_form.split("-")[0]
                if hiragana_katakana_kanji_pattern.match(base_form):
                    vocab.add(base_form)

    return vocab
