#!/usr/bin/env python

from subprocess import check_output, Popen

# Used a bunch of bash-level commands for this tool:
cur_wrksp_cmd     = "wmctrl -d"
wrksp_windows_cmd = "wmctrl -l -G -x"
hl_cmd            = "xrandr | grep 'connected'"
mouse_pos_cmd     = "xdotool getmouselocation"
next_wrksp_cmd    = "xdotool set_desktop -r 1"
move_cmd          = 'xdotool set_desktop_for_window "$WINID" $WRKSP'

def tmpfile_write(data="0,0"):
  with open("/tmp/data", "w") as f:
    f.write(data)
  return data

def tmpfile_read():
  with open("/tmp/data", "r") as f:
    return f.read()

def cmd_call(command):
  return check_output(command, shell=True).decode("utf-8")

def spawn_cmd(command):
  Popen(command, shell=True)
