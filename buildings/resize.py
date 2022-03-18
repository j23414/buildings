#! /usr/bin/env python

# (1) Import Libraries
import sys
import argparse
import os
from glob import glob
from PIL import Image

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
def resize_800width(imgfile:str, outdir:str = 'resized', new_width:int = 800):
  img = Image.open(imgfile)
  if img.mode != 'RGB':
    img = img.convert('RGB')
  width, height = img.size
  
  if width > height: # Ignore landscaped items
    new_img = img
  elif width < 800:  # Ignore smaller images
    new_img = img
  else:              # Resize image
    ratio = height / width
    new_height = int(ratio * new_width)
    new_img = img.resize((new_width, new_height))

  # Save image to new folder
  if not os.path.exists(outdir):
    os.makedirs(outdir)
  new_img.save(outdir + '/' + os.path.basename(imgfile))

# (4) Main call, connecting arguments to reusable functions (workflow)
def main():
    args = parse_args()

    file_list = glob(args.imgs)
    for filename in file_list:
      print(filename)
      resize_800width(filename)

if __name__ == '__main__':
    main()
