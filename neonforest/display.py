from neonforest.immtypes import FourSides
import curses
import time

PAD_FOR_BORDER = 2
STATUS_BAR_HEIGHT = 2

class CursesDisplay():

    def __init__(self, workspace):
        self.workspace = workspace
        self.off_x = 0
        self.off_y = 0
        self.paused = False
        self.display_layer = 'ptrail'
        self.wkpadding = FourSides(top=1, bottom=1, right=1, left=1)

    def display(self):
        curses.wrapper(self.loop)

    def draw_statusbar(self, window):
        window_my, window_mx = window.getmaxyx()
        window.erase()
        pause_str = ""
        if self.paused:
            pause_str = "<PAUSED>"
        status_str = "({},{})\t{}\t{}".format(self.off_x,self.off_y,self.display_layer,pause_str)
        window.addstr(0,0,status_str)
        window.noutrefresh()

    def manage_keys(self, stdscr):
        stdscr_y, stdscr_x = stdscr.getmaxyx()
        c = stdscr.getch()

        if c == curses.KEY_LEFT or c == ord('h'):
            self.off_x = self.off_x - 10
            if self.off_x < 0:
                self.off_x = 0
        elif c == curses.KEY_RIGHT or c == ord('l'):
            self.off_x = self.off_x + 10
            if self.off_x > self.workspace.width - stdscr_x + self.wkpadding.left + self.wkpadding.right + PAD_FOR_BORDER:
                self.off_x = self.workspace.width - stdscr_x + self.wkpadding.left+ self.wkpadding.right + PAD_FOR_BORDER
        elif c == curses.KEY_UP or c == ord('k'):
            self.off_y = self.off_y - 10
            if self.off_y < 0:
                self.off_y = 0
        elif c == curses.KEY_DOWN or c == ord('j'):
            self.off_y = self.off_y + 10
            if self.off_y > self.workspace.height - stdscr_y + self.wkpadding.top + self.wkpadding.bottom + PAD_FOR_BORDER + STATUS_BAR_HEIGHT - 1:
                self.off_y = self.workspace.height - stdscr_y + self.wkpadding.top + self.wkpadding.bottom + PAD_FOR_BORDER + STATUS_BAR_HEIGHT - 1
        elif c == ord('p'):
            self.paused = not self.paused
        elif c == ord('q'):
            stdscr.addstr(stdscr_y-1, 0, "confirm quit (y/n)")
            stdscr.nodelay(False)
            confirm = stdscr.getch()
            if confirm == ord('y'):
                exit()
            stdscr.nodelay(True)


    def loop(self,stdscr):

        stdscr_y, stdscr_x = stdscr.getmaxyx()
        workpad = curses.newpad(self.workspace.width+PAD_FOR_BORDER, self.workspace.height+PAD_FOR_BORDER)
        status_bar = curses.newwin(STATUS_BAR_HEIGHT, stdscr_x+1, stdscr_y - STATUS_BAR_HEIGHT, 0 )
        stdscr.nodelay(True)
        curses.curs_set(0)
        last_t = time.time()

        while True:

            stdscr_y, stdscr_x = stdscr.getmaxyx()
            #control keybinds
            self.manage_keys(stdscr)

            #update status bar
            self.draw_statusbar(status_bar)

            # update simulation
            current_t = time.time()
            if (current_t - last_t) > 0.1 and not self.paused:
                last_t = current_t
                self.workspace.step_all()
                self.workspace.render_to_curses(self.display_layer, workpad)

            stdscr.noutrefresh()
            workpad.noutrefresh(self.off_y,self.off_x,self.wkpadding.top,self.wkpadding.left,stdscr_y-self.wkpadding.bottom-STATUS_BAR_HEIGHT,stdscr_x-self.wkpadding.right-1)

            curses.doupdate()
            time.sleep(0.01666)

