import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from random import randint
start = time.perf_counter()


def doit(num=1):
    print(f'Sleeping for {num} second(s)')
    time.sleep(num)
    return f'Waking up {num}'


def main():
    # OLD METHOD
    # processes = []
    # for _ in range(10):
    #     p = multiprocessing.Process(target=doit, args=(10,))
    #     p.start()
    #     processes.append(p)
    #
    # for p in processes:
    #     p.join()

    # NEW METHOD using context manager
    with ProcessPoolExecutor() as executor:
        results = [executor.submit(doit, randint(1, 10)) for _ in range(5)]

        for f in as_completed(results):
            print(f.result())

if __name__ == '__main__':
    main()
    finish = time.perf_counter()
    print(f'time elapsed {round(finish - start, 2)} second')



