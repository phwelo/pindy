#!/usr/bin/env python3

# NOTE: This is only going to work on dual monitor as I use a line between monitors to differentiate which monitor an app is on.  Further work would be required to add more.  And I don't have more.
# NOTE: I know these commands probably aren't the best/quickest way and intend to improve or ask the community to improve down the road

from os.path import exists
from shared import *
import plasma
from subprocess import Popen
import time

prereqs = ["wmctrl", "xdotool", "xrandr"]

def move_window(window, next):
  cmd_call(move_cmd.replace("$WINID", str(window["id"])).replace("$WRKSP", str(next)))

def init():
  for command in prereqs:
    if not exists("/usr/bin/" + command):
      print("Please install " + command)
      exit(1)
  if not exists("./data"):
    tmpfile_write()
  '''should have already assured this exists, so now we can read it'''
  return tmpfile_read().split(",")

def increase_offset(offset, num=2):
  if int(offset) == num:
    return 0
  return int(offset) + 1

def move_window_group(windows):
  for window in windows:
    move_window(window, window["next_desktop"])

def next_workspace_action():
  offsets = init()
  Screens = plasma.PlasmaDesktop()
  if Screens.mouse_side == "left":
    offsets[0] = increase_offset(offsets[0])
    move_window_group(Screens.right_windows)
  elif Screens.mouse_side == "right":
    move_window_group(Screens.left_windows)
    offsets[1] = increase_offset(offsets[1])
  tmpfile_write(str(offsets[0]) + "," + str(offsets[1]))
  Screens.go_to_next_workspace()
  Popen("pkill feh".split(" "))

def main():
  action = "next_workspace"
  if action == "next_workspace":
    next_workspace_action()
  # would sure be nice to have a reverse action as well

if __name__ == "__main__":
  main()
