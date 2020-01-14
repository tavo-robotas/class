import os
from multiprocessing import Process, current_process


def square(number):
    result = number ** 2
    # OS method getpid is used to get process id assigned
    # to the call of this function that is assigned by the operating system

    # process_id = os.getpid()
    # print(f'Process ID: {process_id}')

    process_name = current_process().name
    print(f'The process name is: {process_name}')
    print(f'the square of {number} is {result}')


if __name__ == '__main__':
    numbers = [2, 4, 6, 8]
    for number in numbers:
        # args = (number,) comma at the end is not a typo it was built that one,
        # although its weird you can google more about it
        process = Process(target=square, args=(number,))

        # Processes are spawned by creating Process object
        # then calling its start() method
        process.start()