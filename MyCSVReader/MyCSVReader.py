#! python

import sys
from Viewer import *
from pathlib import Path

arg_cnt = len(sys.argv)
file = ''

if arg_cnt == 2:
     file = sys.argv[1]

while True:
    if arg_cnt == 1 and file == '':
        file = input("File not selected. Please enter full path to file: ")
    elif file != '' and file[-4:] != '.csv':
        file = input("File not matches to '.csv' or don't exist! Please enter full path to file: ")
    else:
        file = input("Wrong path! Please enter full path to file: ")
     
    if Path(file).is_file():
        break
    
view = Viewer(file)
view.print()

key = ''
while key != ord('q') and key != curses.KEY_EXIT:
    key = view.getch()
    if key == curses.KEY_UP: 
        view.line_up()
    elif key == curses.KEY_DOWN: 
        view.line_down()
    elif key == curses.KEY_LEFT:
        view.page_up()
    elif key == curses.KEY_RIGHT:
        view.page_down()
    elif key == ord('t'):
        view.to_begin()
    elif key == ord('b'):
        view.to_end()

view.exit()
