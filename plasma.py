#!/usr/bin/env python3

from shared import *

# Make a class for easier management
class PlasmaDesktop():
  '''describe the parent element that makes up plasma desktop'''
  def __init__(self):
    self.current_workspace, self.workspaces = self.get_workspace_info()
    self.next_workspace    = self.get_next_workspace()
    self.prev_workspace    = self.get_prev_workspace()
    self.all_windows       = list(self.get_workspace_windows())
    self.horizontal_line   = self.get_horizontal_line()
    self.mouse_side        = self.get_mouse_side()
    self.left_windows      = list(self.get_left_windows())
    self.right_windows     = list(self.get_right_windows())
    self.locked_side       = "left" if self.mouse_side == "right" else "right"

  def get_workspace_info(self):
    '''make this handle current as well as all workspaces to save a call'''
    cur_wrksp = cmd_call(cur_wrksp_cmd)
    workspaces = [i[0] for i in cur_wrksp.splitlines()]
    for line in cur_wrksp.splitlines():
      if "*" in line:
        return line.split()[0], workspaces

  def get_workspace_windows(self):
    '''gets all windows except for those plasmashell ones that screw everything up if you move them anywhere'''
    wrksp_windows = cmd_call(wrksp_windows_cmd)
    for line in wrksp_windows.splitlines():
      # let's ignore this early, i never want to fuck with it and no clue how to reverse when it gets moved to a desktop
      if line.split()[6] != "plasmashell.plasmashell":
        yield {
          "id": line.split()[0],
          "desktop": line.split()[1],
          "next_desktop": int(line.split()[1]) + 1 if line.split()[1] != self.workspaces[-1] else self.workspaces[0],
          "left": line.split()[2],
          "name": line.split()[6]
          }

  def get_next_workspace(self):
    '''get the next workspace, if it's the last, return the first'''
    count = len(self.workspaces)
    if int(self.current_workspace) ==  count - 1:
      return 0
    return int(self.current_workspace) + 1

  def get_prev_workspace(self):
    '''get the previous workspace, if it's first return the last'''
    count = len(self.workspaces)
    if int(self.current_workspace) == 0:
      return count

  def get_horizontal_line(self):
    '''figure out where the horizontal dilineation between monitors is'''
    hl = cmd_call(hl_cmd)
    for line in hl.splitlines():
      if "+" in line and line.split("+")[1] != "0":
        return line.split("+")[1]

  def get_mouse_side(self):
    '''figure out which side of the horizontal line the mouse is on'''
    mouse_pos = cmd_call(mouse_pos_cmd)
    mouse_pos = mouse_pos.split()[0].split(":")[1]
    if int(mouse_pos) < int(self.horizontal_line):
      return "left"
    else:
      return "right"

  def get_left_windows(self):
    '''get all windows on the left side of the horizontal line'''
    for window in self.all_windows:
      if int(window["left"]) < int(self.horizontal_line):
        yield window
  
  def get_right_windows(self):
    '''get all windows on the right side of the horizontal line'''
    for window in self.all_windows:
      if int(window["left"]) > int(self.horizontal_line):
        yield window

  def go_to_next_workspace(self):cmd_call(next_wrksp_cmd)
