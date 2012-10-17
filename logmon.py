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
                if (logger not in self.known_loggers and
                        not isinstance(logger, logging.PlaceHolder)):
                    QUEUE.put('create {}'.format(logger.name))
                    self.known_loggers.add(logger)

            for logger in self.known_loggers:
                if logger not in loggers:
                    QUEUE.put('remove {}'.format(logger.name))


def run_monitor():
    MON = Monitor()
    MON.daemon = True
    MON.start()


def parse_options():
    usage = "logmon.py scriptfile [arg] ..."
    parser = OptionParser(usage=usage)
    parser.allow_interspersed_args = False
    parser.add_option('-d', '--daemonize', action='store_true', default=False,
        help='Run the monitor application as daemon. This will make it '
            'exit automatically once the monitored application finishes. For '
            'the graphical window, you may not want this to happen!')
    parser.add_option('-u', '--ui', default='tk', metavar='UI',
        help='Select the user interface to run. Currently only "tk" is '
            'supported.')

    if not sys.argv[1:]:
        parser.print_usage()
        sys.exit(2)

    (options, args) = parser.parse_args()

    if not args:
        parser.print_usage()
        sys.exit(2)

    return options, args


def execute_script(options, args):

    sys.argv[:] = args

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


def run_ui(ui, daemonize):
    if ui not in ('tk', ):
        print "{0} is an unsupported UI!".format(ui)
        sys.exit(2)

    if ui == 'tk':
        import localui
        t = threading.Thread(target=localui.main, args=(QUEUE,))
        if daemonize:
            t.daemon = True
        t.start()


def main():
    options, args = parse_options()
    run_monitor()
    run_ui(options.ui, options.daemonize)
    execute_script(options, args)


if __name__ == '__main__':
    main()
