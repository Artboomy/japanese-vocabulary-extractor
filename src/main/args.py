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
        help="Provided folder contains multiple volumes. Each folder will be treated as its own volume.",
    )
    parser.add_argument("folder", type=str, help="Path to the folder.")
    return parser.parse_args()
