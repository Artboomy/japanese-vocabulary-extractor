#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# Standard library imports
import regex as re
import logging
from tqdm import tqdm

# Third-party imports (install these with pip)
import MeCab

# Filtering by part of speech (pos) to reduce output
# @see https://www.unixuser.org/~euske/doc/postag/
excluded_pos = [
    # aux verbs - "ない"
    "助動詞",
    # conjunctions - "て", check with startswith
    "助詞",
    # interjections - "ねえ"
    "感動詞",
    # punctuation
    "補助記号",
    # symbols?
    "記号",
    # person's name
    "名詞-固有名詞-人名"
]

def vocab_from_texts(texts: list, freq_order: bool, debug: bool) -> list:
    vocab = []
    mecab = MeCab.Tagger()

    confirm_japanese_pattern = re.compile(r"[\p{IsHiragana}\p{IsKatakana}\p{IsHan}]+")
    katakana_only_pattern = re.compile(r"[\p{IsKatakana}]+")
    pos_map = {}
    debug_file = None
    # file for debugging
    if debug:
        debug_file = open("debug_word_info.log", "w", encoding="utf-8")
    for text in texts:
        parsed = mecab.parse(text)
        words = parsed.split("\n")
        for word in words:
            if debug_file:
                debug_file.write(word + '\n')
            word_info = word.split("\t")
            if word == "EOS" or word == "" or len(word_info) < 4:
                continue
            # The 1st element contains the word itself, while the 4th element contains the base form
            # For some reason the 4th element contains the english translation
            # for katakana-only words, so we differentiate between katakana-only
            # words and other words
            base_form = (
                word_info[0]
                if katakana_only_pattern.match(word_info[0])
                else word_info[3]
            )
            # Sometimes the base form is followed by a hyphen and more text about word type
            base_form = base_form.split("-")[0]
            pos = word_info[4]
            # filter by part of speech
            is_excluded_pos = pos.startswith(tuple(excluded_pos))
            is_pattern_match = confirm_japanese_pattern.match(base_form)
            if not is_excluded_pos and is_pattern_match:
                vocab.append(base_form)
                if debug:
                    if pos in pos_map:
                        if not base_form in pos_map[pos]:
                            pos_map[pos].append(base_form)
                    else:
                        pos_map[pos] = [base_form]
    if debug_file:
        debug_file.write(json.dumps(pos_map, ensure_ascii=False, indent=2) + "\n")
        debug_file.close()

    if freq_order:
        freq = get_word_frequencies(vocab)

    # Remove duplicates from list (not using a set to preserve order)
    vocab = remove_duplicates(vocab)

    if freq_order:
        vocab = sorted(vocab, key=lambda word: freq[word], reverse=True)

    return vocab


def get_word_frequencies(vocab: list):
    freq = dict()
    for word in vocab:
        if word not in freq:
            freq[word] = 0
        freq[word] += 1
    return freq


def remove_duplicates(vocab: list) -> list:
    known_words = set()
    i = 0
    while i < len(vocab):
        if vocab[i] in known_words:
            vocab.pop(i)
            i -= 1
        else:
            known_words.add(vocab[i])
        i += 1
    return vocab
