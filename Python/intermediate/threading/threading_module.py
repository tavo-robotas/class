import time
import threading


def operation(name, delay):

    for i in range(5):
        time.sleep(delay)
        print(f'name of thread {name} ------ {time.time()}')


def square(number):
    print(f'square of {number} is {number**2}')


def cube(number):
    print(f'cube of {number} is {number**3}')


if __name__ == '__main__':
    th1 = threading.Thread(target=square, args=(5,))
    th2 = threading.Thread(target=cube, args=(2,))

    th1.start()
    th2.start()

    th1.join()
    th2.join()

    print('Done')