#! /usr/bin/env python

import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description = "Take a script, return a wdl task"
    )
    parser.add_argument(
        "--script",
        help = "The sequence fasta file.",
        required = True
    )
    parser.add_argument(
        "--docker",
        help = "Docker location.",
        required = False
    )
    return parser.parse_args()

nf_text = """
process {name} {
  input: 
  output: 
  scripts:
  \"\"\"
  {script}
  \"\"\"
}
"""

def mk_nf_task(script, name="example"):
    print(nf_text.format(script=script, name=name))

def main():
    args = parse_args()
    mk_nf_process(args.script, args.docker)

if __name__ == "__main__":
    main()
