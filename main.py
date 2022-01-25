import curses        # cursor module
from curses import wrapper # init curses modeule, it takes over the terminal and its going to allow me to run some different commands also restore the terminal back to previous state
import time
import random

def start_screen(stdscr):
    #stdscr.clear()
    stdscr.addstr("Welcome to the speed typing test!")
    stdscr.addstr("\n Press any key to begin!")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)       # print current txt
    stdscr.addstr(1, 0, f"WPM: {wpm}")
    
    for i, char in enumerate(current):  # i = index, char = value
        correct_char = target[i]        
        if char != correct_char:        # if char doesnt matche RED else GREEN 
            color = curses.color_pair(2)
        else:
            color = curses.color_pair(1)
        stdscr.addstr(0, i, char, color) #start from row 0 and print 

def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip() #strip strips off \n

def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time() # in  seconds LARGE NUMBER; number of seconds passed which is called as EPOC
    stdscr.nodelay(True) # doesnt wait for key 

    while True:    # contuniously ask th user to type something
        time_elpased = max(time.time() -  start_time, 1) # current time - start time!! 1 to avoid divisin by zero error for irst iteration 
        wpm = round((len(current_text)/(time_elpased / 60))/5) #chars per minnute/avgword has 5char runs everytime char is entered

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()      # if the user deosnt type something it crashes to handle use try
        except:
            continue  # if you havnt hit the key no point in run below lines so restart while
        
        if ord(key) == 27: #ordinal valu of the key
            break

         
        if key in ("KEY_BACKSAPCE", '\b', '\x7f'):
            if len(current_text) > 0:
                current_text.pop()
        
        elif len(current_text) < len(target_text):
            current_text.append(key) 

       
        
def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) # init color_pair
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    start_screen(stdscr)
    
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "You completed the text. Press Enter key to continue and esc to quit")
        key = stdscr.getkey()
        
        if ord(key)== 27:
            break

wrapper(main)


