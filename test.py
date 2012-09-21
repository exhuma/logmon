from time import sleep
import logging
for i in range(10):
    print i
    sleep(1)
    if i == 4:
        logging.getLogger('bla')

    if i == 5:
        import foo
        print foo
