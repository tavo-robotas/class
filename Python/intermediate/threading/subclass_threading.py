import time
import threading


def operation(name, delay):

    for i in range(5):
        time.sleep(delay)
        print(f'thread {name} ------ {time.time()}')


class ClassThread(threading.Thread):

    def __init__(self, name, delay):
        threading.Thread.__init__(self)
        self.__name = name
        self.__delay = delay

    def run(self):
        print(f'starting thread {self.__name}')
        operation(self.__name, self.__delay)
        print(f'end of thread {self.__name}')

if __name__ == '__main__':
    th1 = ClassThread('A', 1)
    th2 = ClassThread('B', 2)

    th1.start()
    th2.start()

    # information about threads
    print(th1.getName())
    print(th2.getName())
    print(threading.active_count())
    print(threading.current_thread())
    print(threading.enumerate())

    th1.join()
    th2.join()

    print('Done')
