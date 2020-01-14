import os
from multiprocessing import Process, current_process
import  time

def square(numbers):

    for number in numbers:
        time.sleep(0.5)
        result = number ** 2
        print(f'the square of {number} is {result}')


if __name__ == '__main__':
    numbers = range(100)
    processes = list()
    for i in range(100):
        process = Process(target=square, args=(numbers,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()

    print("multiprocessing complete")