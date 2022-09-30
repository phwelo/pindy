# pindy
Trying to write something to give independent monitor workspaces in KDE Plasma

### What really happens:
Workspace is rotated forward, but the opposite monitor to the mouse gets all of its apps moved forward to the next workspace. A temp file is written with the current offset from active workspace.

## Prereqs:
```
Plasma, probably 5+ I think
["wmctrl", "xdotool", "xrandr"]
Dual Monitors (Two monitors. No more, no less)
```
## Current features:
```
Rotate forward through active window sets on individual monitors
Display current window set number as either `int` (like 1, 2, 3) or `int*{character}` (like *, **, ***)
```

## Feature wishlist:
```
Rotate backward through active window sets on individual monitors  
Native notifier plugin instead of python script
Single Monitor fallback (to maintain shortcuts when laptop undocked)
>2 Monitor Support
Visually freeze the non-switched screen so that we don't have to bear the animations
```

## Usage:
Switch to next workspace, moving any items on the opposite monitor to the workspace that you've just switched to.
```
> ./pindy.py
```

Display pager info for pindy workspaces
```
❯ ./dots.py --help
usage: dots.py [-h] [-d] [-n] [-l] [-r]

options:
  -h, --help   show this help message and exit
  -d, --dots   Show dots
  -n, --num    Just show number instead of dots
  -l, --left   Move window to left workspace
  -r, --right  Move window to right workspace
```

### Examples

Display a dot for each left side window set
```
./dots.py -l -d
```

Display an integer representation of the right side window set
```
./dots.py -r -n
```
