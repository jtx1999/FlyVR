"""
A class to implement a stopwatch in a tkinter frame

From: http://code.activestate.com/recipes/124894-stopwatch-in-tkinter/
"""

from tkinter import *
from tkinter import ttk
import time


class StopWatch(Frame):
    """ Implements a stop watch frame widget. """

    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self._start = 0.0
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()
        self.makeWidgets()

    def makeWidgets(self):
        """ Make the time label. """
        l = ttk.Label(self, textvariable=self.timestr)
        self._setTime(self._elapsedtime)
        l.pack(fill=X, expand=NO)

    def _update(self):
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)

    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap / 60)
        seconds = int(elap - minutes * 60.0)
        hseconds = int((elap - minutes * 60.0 - seconds) * 100)
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))

    def start(self):
        """ Start the stopwatch, ignore if running. """
        if not self._running:
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1

    def stop(self):
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)
            self._elapsedtime = time.time() - self._start
            self._setTime(self._elapsedtime)
            self._running = 0

    def reset(self):
        """ Reset the stopwatch. """
        self._start = time.time()
        self._elapsedtime = 0.0
        self._setTime(self._elapsedtime)


def main():
    root = Tk()
    sw = StopWatch(root)
    sw.pack(side=TOP)

    Button(root, text='Start', command=sw.start).pack(side=LEFT)
    Button(root, text='Stop', command=sw.stop).pack(side=LEFT)
    Button(root, text='Reset', command=sw.reset).pack(side=LEFT)
    Button(root, text='Quit', command=root.quit).pack(side=LEFT)

    root.mainloop()


if __name__ == '__main__':
    main()
