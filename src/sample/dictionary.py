#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
# Standard Library Imports
import logging
import regex as re
from jamdict import Jamdict
import sys
from collections import defaultdict

class Dictionary(object):
    def __init__(self):
        self.term_meta_bank = defaultdict(list)
        with open('./input/term_meta_bank_1.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(data[0])
            for entry in data:
                word = entry[0]
                # if word in self.term_meta_bank:
                #     print(f'Duplicate term {word} in vocabulary')
                data = entry[2]
                if "frequency" in data:
                    self.term_meta_bank[word].append(data["frequency"]["displayValue"])
                else:
                    self.term_meta_bank[word].append(data["displayValue"])

    def find_term(self, term):
        return self.term_meta_bank.get(term, [])


lookup_dict = Dictionary()


# todo filter by pos
# filter by freq
# filter by archaik/rare?

def get_jamdict_instance():
    # @see https://jamdict.readthedocs.io/_/downloads/en/latest/pdf/
    # High-performance tuning
    # Requires pre-release version puchikarui==0.2a1
    jam = Jamdict(memory_mode=True)
    return jam


def print_jmdict_object(obj, indent=0, visited=None, output_file=sys.stdout):
    """
    Recursively print the attributes of a Jamdict/JMDict object as a tree.
    Writes the output to 'output_file' instead of console.
    Avoids infinite loops by keeping track of visited objects.
    """
    if visited is None:
        visited = set()
    # Prevent re-printing the same object in case of cyclical references
    if id(obj) in visited:
        print("  " * indent + f"<Already visited {obj.__class__.__name__} object>", file=output_file)
        return
    visited.add(id(obj))

    # If this is a Jamdict (or any custom) object with __dict__, explore its fields
    if hasattr(obj, "__dict__"):
        # Print object type and representation
        print("  " * indent + f"{obj.__class__.__name__} -> {obj}", file=output_file)
        # Recursively print each attribute
        for attr_name, attr_value in vars(obj).items():
            print("  " * (indent + 1) + f"{attr_name}:", file=output_file)
            print_jmdict_object(attr_value, indent + 2, visited, output_file)
    elif isinstance(obj, list):
        # If it's a list, print each item
        print("  " * indent + f"List[{len(obj)}]", file=output_file)
        for i, item in enumerate(obj):
            print("  " * (indent + 1) + f"[{i}]:", file=output_file)
            print_jmdict_object(item, indent + 2, visited, output_file)
    elif isinstance(obj, dict):
        # If it's a dict, print each key-value pair
        print("  " * indent + f"Dict ({len(obj)} keys)", file=output_file)
        for k, v in obj.items():
            print("  " * (indent + 1) + f"{k}:", file=output_file)
            print_jmdict_object(v, indent + 2, visited, output_file)
    else:
        # For simple types (str, int, None, etc.)
        print("  " * indent + repr(obj), file=output_file)


hiragana_only_pattern = re.compile(r"[\p{IsHiragana}]+")


def get_word_info(word: str, jam, log_file=sys.stdout, pos="") -> dict:
    result = jam.lookup(word)
    print(f"-----word: {word}-------freq: {lookup_dict.find_term(word)}", file=log_file)
    # if word == "まま":
    #     with open("jmdict_debug.txt", "w", encoding="utf-8") as f:
    #         print(f"=== Jamdict Lookup Tree for '{word}' ===\n", file=f)
    #         for i, entry in enumerate(result.entries):
    #             print(f"\n--- Entry #{i + 1} ---", file=f)
    #             print_jmdict_object(entry, output_file=f)
    # print(f"-----***-------")
    if len(result.entries) == 0:
        return {"definition": "", "kana": "", "is_real": False, "id": "", "frequency": ""}
    pos = pos.lower()
    if hiragana_only_pattern.match(word):
        #     choose better fitting
        best_entry = None
        min_frequency = None
        for entry in result.entries:
            for sense in entry.senses:
                # pos check
                filtered_pos = sense.pos
                if pos:
                    filtered_pos = [x for x in sense.pos if pos in x]
                if not len(filtered_pos):
                    print(f"No pos found for {entry}, given pos={pos}", file=log_file)
                    continue
                for kanji_form in entry.kanji_forms:
                    freq_list = lookup_dict.find_term(kanji_form.text)
                    normalized_kana_freq = [int(re.search(r'\d+', x).captures()[0]) for x in freq_list if '㋕' in x]
                    print(f"{kanji_form} freq_list={freq_list}, normalized_kana_freq: {normalized_kana_freq}", file=log_file)
                    if not len(normalized_kana_freq):
                        print(f"No kana freq data, skipping {kanji_form}", file=log_file)
                        continue
                    freq = min(normalized_kana_freq)
                    if not min_frequency:
                        min_frequency = freq
                        best_entry = entry
                    elif freq < min_frequency:
                        min_frequency = freq
                        best_entry = entry
                    print(f"Kanji form: {kanji_form.text} frequency: {freq_list}", file=log_file)
                if not len(entry.kanji_forms):
                    freq_list = lookup_dict.find_term(word)
                    normalized_kana_freq = [int(re.search(r'\d+', x).captures()[0]) for x in freq_list if '㋕' in x]
                    if len(normalized_kana_freq):
                        min_frequency = min(normalized_kana_freq)
                        best_entry = entry
                print("Sense glosses:", sense.gloss, file=log_file)
                print("Sense POS tags:", sense.pos, file=log_file)  # <-- Here are the POS tags
            for kana_forms in entry.kana_forms:
                print(f"Kana form: {kana_forms.text} frequency: {lookup_dict.find_term(kana_forms.text)}", file=log_file)
            print(f"Current best frequency: {min_frequency}, best sense: {best_entry}", file=log_file)
            print("****************", file=log_file)
        # if not best_entry:
        #     print(f"No best entry candidate") #, choosing first from {len(result.entries)} entries", file=log_file)
            # best_entry = result.entries[0]
        print('Chosen sense:', best_entry, file=log_file)
        definitions = best_entry
    else:
        definitions = result.entries[0]
    if not definitions:
        print(f"No definitions found for {word}", file=log_file)
        print("---------------", file=log_file)
        return {"definition": "", "kana": "", "is_real": False, "id": "", "frequency": ""}

    definition_text = ", ".join(' / '.join(sense.text().split('/')) for sense in definitions.senses[:3])
    kana_text = definitions.kana_forms[0].text
    print("---------------", file=log_file)
    return {
        "definition": definition_text,
        "kana": kana_text,
        "is_real": True,
        "id": definitions.idseq,
        "frequency": " / ".join(lookup_dict.find_term(word)),
    }
