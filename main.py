#!/usr/bin/env python3

import subprocess

# Parent for all of this
class PlasmaDesktop():
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
    cur_wrksp_cmd = "wmctrl -d"
    cur_wrksp = subprocess.check_output(cur_wrksp_cmd, shell=True)
    cur_wrksp = cur_wrksp.decode("utf-8")
    workspaces = [i[0] for i in cur_wrksp.splitlines()]
    for line in cur_wrksp.splitlines():
      if "*" in line:
        return line.split()[0], workspaces

  def get_workspace_windows(self):
    wrksp_windows_cmd = "wmctrl -l -G -x"
    wrksp_windows = subprocess.check_output(wrksp_windows_cmd, shell=True)
    wrksp_windows = wrksp_windows.decode("utf-8")
    for line in wrksp_windows.splitlines():
      # let's ignore this early, i never want to fuck with it
      if line.split()[6] != "plasmashell.plasmashell":
        yield {
          "id": line.split()[0],
          "desktop": line.split()[1],
          "next_desktop": int(line.split()[1]) + 1 if line.split()[1] != self.workspaces[-1] else self.workspaces[0],
          "left": line.split()[2],
          "name": line.split()[6]
          }

  def get_next_workspace(self):
    count = len(self.workspaces)
    if int(self.current_workspace) ==  count - 1:
      return 0
    return int(self.current_workspace) + 1

  def get_prev_workspace(self):
    count = len(self.workspaces)
    if int(self.current_workspace) == 0:
      return count

  def get_horizontal_line(self):
    hl_cmd = "xrandr | grep 'connected'"
    hl = subprocess.check_output(hl_cmd, shell=True)
    hl = hl.decode("utf-8")
    for line in hl.splitlines():
      if "+" in line and line.split("+")[1] != "0":
        return line.split("+")[1]

  def get_mouse_side(self):
    mouse_pos_cmd = "xdotool getmouselocation"
    mouse_pos = subprocess.check_output(mouse_pos_cmd, shell=True)
    mouse_pos = mouse_pos.decode("utf-8").split()[0].split(":")[1]
    if int(mouse_pos) < int(self.horizontal_line):
      return "left"
    else:
      return "right"

  def get_left_windows(self):
    for window in self.all_windows:
      if int(window["left"]) < int(self.horizontal_line):
        yield window
  
  def get_right_windows(self):
    for window in self.all_windows:
      if int(window["left"]) > int(self.horizontal_line):
        yield window

  def go_to_next_workspace(self):
    next_wrksp_cmd = "xdotool set_desktop -r 1"
    subprocess.call(next_wrksp_cmd, shell=True)

def move_window(window, next):
  move_cmd = 'xdotool set_desktop_for_window "$WINID" $WRKSP'
  subprocess.call(move_cmd.replace("$WINID", str(window["id"])).replace("$WRKSP", str(next)), shell=True)

def main():
  Screens = PlasmaDesktop()
  if Screens.mouse_side == "left":
    for window in Screens.right_windows:
      move_window(window, window["next_desktop"])
  elif Screens.mouse_side == "right":
    for window in Screens.left_windows:
        move_window(window, window["next_desktop"])
  Screens.go_to_next_workspace()

if __name__ == "__main__":
  main()
