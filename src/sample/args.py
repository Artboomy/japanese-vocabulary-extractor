#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def parse_arguments():
    """Parse command-line arguments."""
    import argparse

    parser = argparse.ArgumentParser(
        description="This script allows you to extract a vocabulary list from a folder of manga images."
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
        help="Type of input. Can be 'manga', 'pdf', 'epub' or 'text'. If manga, you must provide a folder. Otherwise provide the file or a folder of multiple files.",
    )
    parser.add_argument(
        "input_path",
        type=str,
        help="Path to the folder or file to be scanned.",
    )
    return parser.parse_args()
