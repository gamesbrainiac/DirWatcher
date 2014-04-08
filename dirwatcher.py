# encoding=utf-8

import os
import time
import threading
import sys

from queue import Queue

from clint.textui import colored, puts

MAIN_TASK_QUEUE = Queue()


def watch(directory):
    print("Watching {}".format(directory))
    old = set(os.listdir(directory))
    while True:
        time.sleep(0.5)
        new = set(os.listdir(directory))
        change = old ^ new
        if change:
            old = new
            for c in change:
                MAIN_TASK_QUEUE.put(c)


def print_q():
    while MAIN_TASK_QUEUE:
        change = MAIN_TASK_QUEUE.get()
        try:
            assert isinstance(change, str)
            print(change.split('__')[0])
            sys.stdout.write('\a')
            sys.stdout.flush()
        except (AssertionError,):
            print("{} is not a string".format(change))

if __name__ == '__main__':
    # dirs = sys.argv[1:]  # This is for command line arguments
    dirs = [r'/Users/quazinafiulislam/Code/Python/DirWatcher', r'/Users/quazinafiulislam/Downloads']
    for d in dirs:
        threading.Thread(target=watch, args=(d,), daemon=True).start()
    threading.Thread(target=print_q, args=(), daemon=True).start()
    puts(colored.yellow('Press') + ' ' + colored.yellow('q', bold=True) + ' ' + colored.yellow('to quit.'))
    if input() == 'q': pass