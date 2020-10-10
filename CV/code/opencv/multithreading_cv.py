import cv2 as cv
from streamer import Stream
from viewer import View
from counter import Counter
import concurrent.futures


def place(frame, elapsed):
    if elapsed:
        cv.putText(frame, f"{elapsed:.0f} iterations/sec", (10, 450), cv.FONT_HERSHEY_SIMPLEX,
                   1.0, (255, 255, 255))
    return frame


def threading(source=1):
    stream  = Stream(source).start()
    view = View(frame=stream.frame, name=str(source)).start()
    cps  = Counter().start()
    while True:
        if stream.stopped or view.stopped:
            break
        frame = stream.frame
        frame = place(frame, cps.count())
        view.frame = frame
        cps.increment()


def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
         s1 = executor.submit(threading, 0)
         s2 = executor.submit(threading, 2)


if __name__ == "__main__":
    main()
