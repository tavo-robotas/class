import threading

storage = {
    'a': 0,
    'b': 0,
    'c': 0,
    'd': 0,
    'e': 0,
    'f': 0
}
x = 0

def task(lock):
    # global storage
    # numbers = [10, 100, 1000, 10000, 100000, 1000000]
    # for number in numbers:
    #     for i in range(number):
    #         for k, v in storage.items():
    #             storage[k] = v + 1
    global x
    number = 1000000
    for i in range(number):
        lock.acquire()
        x += 1
        lock.release()


def main():
    lock = threading.Lock()

    th1 = threading.Thread(target=task, args=(lock,))
    th2 = threading.Thread(target=task, args=(lock,))

    th1.start()
    th2.start()
    th1.join()
    th2.join()


if __name__ == '__main__':
    main()
    print(f'{x}')
    # print(f'{storage}')

