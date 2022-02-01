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

wdl_text = """
task {name} {
  input {
  }
  ouptut {
  }
  command {
    {script}
  }
  runtime {
    docker: {docker}
  }
}
"""

def mk_wdl_task(script, docker, name="example"):
    print(wdl_text.format(script=script, name=name, docker=docker))

def main():
    args = parse_args()
    mk_wdl_task(args.script, args.docker)

if __name__ == "__main__":
    main()
