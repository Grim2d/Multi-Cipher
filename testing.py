import curses
from curses.textpad import Textbox, rectangle
from curses import wrapper


'''
begin_x = 20; begin_y = 7
height = 5; width = 40
win = curses.newwin(height, width, begin_y, begin_x)
'''





def run_gui(stdscr):
    stdscr.clear()
    win = curses.newwin(25, 80, 1, 1)
    rectangle(stdscr, 0, 0, 23, 79)
    status = "Application started successfully."
    stdscr.addstr(24, 0, 'Status: ' + status)
    win.refresh()
    stdscr.getkey()

if __name__ == "__main__":
    wrapper(run_gui)