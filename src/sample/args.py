#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def parse_arguments():
    """Parse command-line arguments."""
    import argparse

    parser = argparse.ArgumentParser(
        description="This script allows you to extract a vocabulary list with or without english definitions from various types of japanese media."
    )
    parser.add_argument(
        "--parent",
        action="store_true",
        help="Only relevant if processing a manga: provided folder contains multiple volumes. Each folder will be treated as its own volume.",
    )
    parser.add_argument(
        "--add-english",
        action="store_true",
        help="Looks up and adds the English translation of each word to the CSV file.",
    )
    parser.add_argument(
        "--type",
        type=str,
        required=True,
        help="Type of input. Can be 'manga', 'subtitle', 'pdf', 'epub', 'txt' or 'generic'. If manga, you must provide a folder. Otherwise provide the file or a folder of multiple files. Generic just scans through any files it finds (or the file provided) and tries to extract words from them.",
    )
    parser.add_argument(
        "input_path",
        type=str,
        help="Path to the folder or file to be scanned.",
    )
    return parser.parse_args()
