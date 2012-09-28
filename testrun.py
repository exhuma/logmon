from cmd import Cmd
import logging
import sys
LOG = logging.getLogger(__name__)


class MyCmd(Cmd):

    def do_EOF(self, line):
        LOG.warning("Exiting")
        print ""
        sys.exit(0)

    def do_hello(self, line):
        LOG.info("Hello")

    do_exit = do_EOF

if __name__ == '__main__':

    app = MyCmd()
    app.cmdloop()
