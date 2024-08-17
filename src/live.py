from pathlib import Path

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import subprocess
import sys

FILE = Path(sys.argv[1]).resolve()

CWD = FILE.parent

CMD = "exec python " + str(FILE)


class MyEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global PROC
        PROC.kill()


event_handler = MyEventHandler()
observer = Observer()
observer.schedule(event_handler, str(CWD), recursive=True)
observer.start()

try:
    while True:
        PROC = subprocess.Popen(CMD, shell=True)
        PROC.wait()
        time.sleep(0.1)
finally:
    observer.stop()
    observer.join()
