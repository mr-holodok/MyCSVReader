import curses
from Reader import *

class Viewer(object):
    def __init__(self, file_name):
        self.__stdscr = curses.initscr() # Initialization
        curses.noecho()                # read-only type (writting from keyboard not allowed)
        curses.cbreak()                # react to keys instantly, without requiring the Enter key to be pressed; 
        self.__stdscr.keypad(1)          # enable processing special sequences (button up etc...)
        curses.start_color()           # enable colored console
        self.__height, self.__width = self.__stdscr.getmaxyx() # height and width of console (in characters) 
        self.__file = file_name 
        self.__reader = Reader(self.__file, self.__height - 6) # file reader
        self.__header = self.__reader.read_head()          # header is a first row of csv file (table hat)
        self.__page = self.__reader.to_begin()               # page holds all rows for current page
        self.__line = 0                  # line holds the value of highlighted row (min value = 0, max = console height - spaces)
        self.__stdscr.clear()            
        self.__stdscr.refresh()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_CYAN)
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)

    def print(self):
        self.__stdscr.clear()            # clear all content of console
        self.__stdscr.addstr(0,(self.__width - len(self.__file))//2, 'File: ' + self.__file, curses.color_pair(1)) # add file name at the console top
        self.__stdscr.addstr(2,0, self.build_line(self.__header), curses.color_pair(2)) # add table header
        c = 3                          # line (in range of console height) where file output starts
        for i in self.__page:            # page holds rows of current page. i is row
            self.__stdscr.addstr(c,0, self.build_line(i)) # add string to line c. build_line crete row with spaces and table delimeters
            c += 1
        self.__stdscr.addstr(self.__line + 3,0, self.build_line(self.__page[self.__line]), curses.color_pair(3)) # add string that represent current line (with another color)
        self.__stdscr.addstr(self.__height - 1,0, " | \u2190 - Page Up | \u2191 - Line Up | \u2192 - Page Down | \u2193 - Line Down | T - to top | B - to bottom | q - to exit |", curses.color_pair(4))
        self.__stdscr.refresh() 

    def line_up(self):                 # reads line that above the page
        if self.__line != 0: self.__line -= 1 # if line is not 0 there is no need to change current page and we only change current line
        else: 
            self.__page = self.__reader.readln(False) # refresh the page
        self.print()

    def line_down(self):               # reads line that under the page  
        if self.__line + 1 != self.__reader.get_block_size(): 
            self.__line += 1 # if line + 1 is not equal to page height 
        else:
            self.__page = self.__reader.readln(True) # if selected row is the last then update page 
        self.print()

    def page_down(self):               # reads next page
        self.__page = self.__reader.readpg(True)
        self.__line = self.__reader.get_block_size() - 1 # current line is the last line at the page
        self.print()

    def page_up(self):                 # reads previous page
        self.__page = self.__reader.readpg(False)
        self.__line = 0                  # current line is the first line at the page
        self.print()

    def to_begin(self):                # reads first page
        self.__page = self.__reader.to_begin()
        self.__line = 0
        self.print()

    def to_end(self):                  # reads last page
        self.__page = self.__reader.to_end()
        self.__line = self.__reader.get_block_size() - 1
        self.print()

    def exit(self):                    # changes console state to normal
        curses.nocbreak()
        self.__stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def build_line(self, row):         # builds line from row (in list presentation) with spaces and delimeters
        str = '|'
        i = 0
        for item in row:
            str += item + (self.__reader.widths[i] - len(item)) * ' ' + '|'
            i += 1
        return str

    def getch(self):
        return self.__stdscr.getch()
