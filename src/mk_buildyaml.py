#! /usr/bin/env python

import sys
import argparse
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(
        description = "Take a sequence and metadata file pair, and return a basic build.yaml"
    )
    parser.add_argument(
        "--sequence",
        help = "The sequence fasta file.",
        required = True
    )
    parser.add_argument(
        "--metadata",
        help = "The metadata tsv file.",
        required = True
    )
    return parser.parse_args()

def main():
    args = parse_args()


if __name__ == "__main__":
    main()
