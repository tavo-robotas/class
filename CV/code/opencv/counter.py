from datetime import datetime
import pdb

class Counter:
    """
    Class that track the number of occurrences ("counts") of an
    arbitrary event and returns the frequency in occurrences ("counts")
    per second. The caller must increment the count.
    """

    def __init__(self):
        self.time = None
        self.occurrences = 0

    def start(self):
        self.time = datetime.now()
        return self

    def increment(self):
        """
        At the end of each iteration of the while loop,
        we’ll call increment() to increment the count.
        """
        self.occurrences += 1

    def count(self):
        """
        During each iteration, we’ll obtain the average iterations/second
        for the video with a call to the count() method.
        """

        duration = (datetime.now() - self.time).total_seconds()
        if duration:
            return self.occurrences / duration

