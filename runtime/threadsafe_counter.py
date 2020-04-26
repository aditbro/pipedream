# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import container
import threading

"""
Implementation of a thread-safe counter with many producers and many consumers.
"""
class Counter:
    def __init__(self, initial_count):
        self.count = initial_count
        self.cv = threading.Condition()
        self.error = None

    def decrement(self):
        self.cv.acquire()
        self.count -= 1
        self.cv.notify_all()
        self.cv.release()

    def add_error(self, error):
        container.terminate()
        if not self.error:
            self.error = error

    def wait(self):
        self.cv.acquire()
        while self.count > 0:
            self.cv.wait()
        self.cv.release()
