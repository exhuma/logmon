import logging
LOG = logging.getLogger(__name__)
logging.getLogger("a")
logging.getLogger("b")
logging.getLogger("c")
logging.getLogger("d").info("inf Hello World!")
logging.getLogger("e")
logging.getLogger("f")

from time import sleep
sleep(3)
l = logging.getLogger('x')
sleep(1)
l.warning('warn')
sleep(3)
