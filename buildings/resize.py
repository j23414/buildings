#! /usr/bin/env python

# (1) Import Libraries
import sys
import argparse
import pandas as pd   # tab delimited files
from PIL import Image
import os
from glob import glob

# (2) Define command line arguments
def parse_args():
    # Main help command
    parser = argparse.ArgumentParser(
        description = "USAGE: python resize.py --imgs 'imgs/*.jpg'"
    )
    # Add first argument
    parser.add_argument(
        "--imgs",
        help = "Path to image or images.",
        required = True
    )

    return parser.parse_args()

# (3) Reusable functions
def resize_800width(imgfile):
  i = Image.open(imgfile)
  if i.mode != 'RGB':
    i = i.convert('RGB')
  width, height = i.size
  if width > height:
    i.save("resized/" + os.path.basename(imgfile))  # Ignore landscapped items
    return
  ratio = height / width
  new_width = 800
  new_height = int(ratio * new_width)
  new_i = i.resize((new_width, new_height))
  new_i.save("resized/" + os.path.basename(imgfile))

# (4) Main call, connecting arguments to reusable functions (workflow)
def main():
    args = parse_args()

    file_list = glob(args.imgs)
    for filename in file_list:
      print(filename)
      resize_800width(filename)

if __name__ == '__main__':
    main()