#!/usr/bin/env python3

from pindy import tmpfile_read
import argparse

def arguments():
  parser = argparse.ArgumentParser()
  parser.add_argument("-d", "--dots", help="Show dots", default=True, action="store_true")
  parser.add_argument("-n", "--num", help="Just show number instead of dots", default=False, action="store_true")
  parser.add_argument("-l", "--left", help="Move window to left workspace", action="store_true")
  parser.add_argument("-r", "--right", help="Move window to right workspace", action="store_true")
  return parser.parse_args()

def checks(args):
  if args.left and args.right:
    print("Please choose left or right, not both")
    exit(1)
  if not args.left and not args.right:
    print("Please choose left or right")
    exit(1)

def num_display(args, offsets):
  if args.left:
    print(str(int(offsets[0]) + 1))
    exit(0)
  if args.right:
    print(str(int(offsets[1]) + 1))
    exit(0)

def print_chars(num, char):
  for i in range(num):
    print(char, end="")
  exit(0)

def main():
  offsets = tmpfile_read().split(",")
  args = arguments()
  checks(args)
  if args.num:
    num_display(args, offsets)
  if args.dots:
    if args.left:
      print_chars(int(offsets[0]) + 1, "ךּ")
    if args.right:
      print_chars(int(offsets[1]) + 1, "ךּ")

if __name__ == "__main__":
  main()