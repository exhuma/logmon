import threading
import os
import logging
import sys
from Queue import Queue
from optparse import OptionParser


QUEUE = Queue()


class Monitor(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(Monitor, self).__init__(*args, **kwargs)
        self.known_loggers = set()

    def run(self):
        while True:
            loggers = logging.getLogger().manager.loggerDict.values()
            for logger in loggers:
                if logger not in self.known_loggers:
                    QUEUE.put('create {}'.format(logger.name))
                    self.known_loggers.add(logger)

            for logger in self.known_loggers:
                if logger not in loggers:
                    QUEUE.put('remove {}'.format(logger.name))


def run_monitor():
    MON = Monitor()
    MON.daemon = True
    MON.start()


def execute_script():
    usage = "logmon.py scriptfile [arg] ..."
    parser = OptionParser(usage=usage)
    parser.allow_interspersed_args = False

    if not sys.argv[1:]:
        parser.print_usage()
        sys.exit(2)

    (options, args) = parser.parse_args()
    sys.argv[:] = args

    if len(args) > 0:
        progname = args[0]
        sys.path.insert(0, os.path.dirname(progname))
        with open(progname, 'rb') as fp:
            code = compile(fp.read(), progname, 'exec')
        globs = {
            '__file__': progname,
            '__name__': '__main__',
            '__package__': None,
        }
        exec code in globs, None
    else:
        parser.print_usage()
    return parser


def main():
    run_monitor()
    execute_script()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    import localui
    t = threading.Thread(target=localui.main, args=(QUEUE,))
    t.daemon = True
    t.start()
    main()
