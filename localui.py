"""
TK Interface for log monitor
"""

import Tkinter as tk
import threading
import logging
from Queue import Empty


OP_CREATE = 1
OP_REMOVE = 2


class TkHandler(logging.Handler):

    def __init__(self, widget, *args, **kwargs):
        logging.Handler.__init__(self)
        self.widget = widget
        self.setLevel(logging.NOTSET)

    def emit(self, record):
        msg = "%s\n" % self.format(record)
        self.widget.insert('1.0', msg)
        self.flush()


def parse_message(msg):
    if msg.startswith('create'):
        operation = OP_CREATE
        payload = msg[7:]
    elif msg.startswith('remove'):
        operation = OP_REMOVE
        payload = msg[7:]
    return (operation, payload)


class App(object):

    def __init__(self, master, queue):

        frame = tk.Frame(master)
        frame.pack()

        self.logwindow = tk.Text(frame)
        self.logwindow.pack(side=tk.LEFT)

        self.logger_list = tk.Listbox(frame)
        self.logger_list.pack(side=tk.RIGHT)

    def worker(self, app, queue):
        while True:
            try:
                item = queue.get_nowait()
                self.logger_list.insert(tk.END, item)
                op, payload = parse_message(item)
                log = logging.getLogger(payload)
                log.addHandler(TkHandler(app.logwindow))
                log.info('Attached looger {0} to monitor.'.format(payload))
                queue.task_done()
            except Empty:
                pass


def main(queue):
    root = tk.Tk()
    app = App(root, queue)
    t = threading.Thread(target=app.worker, args=(app, queue))
    t.daemon = True
    t.start()
    root.mainloop()
