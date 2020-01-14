# synonyms mutex
# more on lock
# https://en.wikipedia.org/wiki/Lock_(computer_science)

import time
from multiprocessing import Process, Lock, Value, log_to_stderr, get_logger
import logging


def add_no_mp(total):
    for i in range(100):
        time.sleep(0.01)
        total += 5
    return total


def sub_no_mp(total):
    for i in range(100):
        time.sleep(0.01)
        total -= 5
    return total


def add_lock(total, block):
    for i in range(100):
        time.sleep(0.01)
        block.acquire()
        total.value += 5
        block.release()


def sub_lock(total, block):
    for i in range(100):
        time.sleep(0.01)
        block.acquire()
        total.value -= 5
        block.release()


if __name__ == '__main__':

    # number = 500
    number = Value('i', 500)
    lock = Lock()
    # print(number)
    # total = add_no_mp(number)
    # print(total)
    # total = sub_no_mp(number)
    # print(total)

    log_to_stderr()
    logger = get_logger()
    logger.setLevel(logging.INFO)

    add_process = Process(target=add_lock, args=(number, lock))
    sub_process = Process(target=sub_lock, args=(number, lock))

    add_process.start()
    sub_process.start()

    add_process.join()
    sub_process.join()

    print(number.value)



