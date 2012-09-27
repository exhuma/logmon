import logging
LOG = logging.getLogger(__name__)
logging.getLogger("a")
logging.getLogger("b")
logging.getLogger("c")
logging.getLogger("d")
logging.getLogger("e")
logging.getLogger("f")

from time import sleep
sleep(5)
