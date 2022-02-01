#! /usr/bin/env python

import sys
import argparse

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

build_text = """
inputs:
- name: {build}
  metadata: {metadata_tsv}
  sequences: {sequence_fasta}
- name: references
  metadata: data/references_metadata.tsv
  sequences: data/references_sequences.fasta
"""

def mk_buildyaml(sequence_fasta, metadata_tsv, build="example"):
    print(build_text.format(sequence_fasta = sequence_fasta, metadata_tsv = metadata_tsv, build = build))

def main():
    args = parse_args()
    mk_buildyaml(args.sequence, args.metadata)

if __name__ == "__main__":
    main()
