import json
import logging
from typing import Any

import regex as re

import spacy

excluded_pos2 = [
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
# https://spacy.io/usage/linguistic-features
included_pos = [
    "NOUN",
    "VERB",
    # only with kanji?
    "PRON",
    "ADJ",
    "ADV",
    # longer than 2 chars?
    "CCONJ",
]

excluded_pos = [
    "PUNCT",
    "ADP",
    "PART",
    "AUX",
    "SYM",
    "NUM",
    "X",
    "SCONJ",
    # kono / sono / ano
    "DET",
    # personal names
    "PROPN",
    "INTJ",
]


def vocab_from_texts(texts: list, freq_order: bool, debug: bool) -> tuple[list[Any] | list, dict[Any, int]]:
    vocab = []
    confirm_japanese_pattern = re.compile(r"[\p{IsHiragana}\p{IsKatakana}\p{IsHan}]+")
    hiragana_only_pattern = re.compile(r"[\p{IsHiragana}]+")
    nlp = spacy.load('ja_ginza_electra')
    debug_file = open("debug_word_info2.log", "w", encoding="utf-8")
    for text in texts:
        doc = nlp(text)
        for token in doc:
            lemma = token.norm_ if token.pos_ == "VERB" else token.lemma_
            hiragana_only = hiragana_only_pattern.match(lemma)
            if len(lemma) < 2 and hiragana_only:
                # logging.info(f"Skipped {lemma}")
                continue
            pos = token.pos_
            if pos not in included_pos and pos not in excluded_pos:
                print('UNKNOWN POS', pos)
            pos_ok = pos in included_pos
            if pos == "PRON":
                pos_ok = pos_ok and not hiragana_only_pattern.match(lemma)
            if pos == "CCONJ":
                pos_ok = pos_ok and len(lemma) > 2
            if confirm_japanese_pattern.match(lemma) and pos_ok:
                vocab.append((lemma, token.norm_, token.pos_))
            debug_file.write(" ".join([
                f"i={token.i}",
                f"orth={token.orth_}",
                f"lemma_={token.lemma_}",
                f"norm_={token.norm_}",
                f"reading={token.morph.get("Reading")}",
                f"pos={token.pos_}",
                f"Inflection={token.morph.get("Inflection")}",
                f"tag_={token.tag_}",
                f"dep_={token.dep_}",
                f"head.i={token.head.i}",
                "\n"
            ]))

    freq = get_word_frequencies(vocab)

    # Remove duplicates from list (not using a set to preserve order)
    vocab = remove_duplicates(vocab)

    if freq_order:
        vocab = sorted(vocab, key=lambda word: freq[word], reverse=True)

    return vocab, freq,


def get_word_frequencies(vocab: list):
    freq = dict()
    for word, _, _ in vocab:
        if word not in freq:
            freq[word] = 0
        freq[word] += 1
    return freq


def remove_duplicates(vocab: list) -> list:
    known_words = set()
    i = 0
    while i < len(vocab):
        if vocab[i][0] in known_words:
            vocab.pop(i)
            i -= 1
        else:
            known_words.add(vocab[i][0])
        i += 1
    return vocab
