# Copyright (c) 2010 Peter Teichman
# Copyright (c) 2011 litl, LLC

import time

from contextlib import contextmanager

class Tracer(object):
    def __init__(self, reporter=None):
        self.reporters = []
        if reporter is not None:
            self.add_reporter(reporter)

    def add_reporter(self, reporter):
        self.reporters.append(reporter)

    @staticmethod
    def now_us():
        """Microsecond resolution, integer now"""
        return int(time.time() * 1000 * 1000)

    @staticmethod
    def now_ms():
        """Millisecond resolution, integer now"""
        return int(time.time() * 1000)

    def trace(self, stat, value, user_data=None):
        for reporter in self.reporters:
            reporter.trace(stat, value, user_data)

    @contextmanager
    def trace_us(self, stat, user_data=None):
        start = self.now_us()
        yield
        end = self.now_us()
        self.trace(stat, end - start, user_data)

    @contextmanager
    def trace_ms(self, stat, user_data=None):
        start = self.now_ms()
        yield
        end = self.now_ms()
        self.trace(stat, end - start, user_data)

    def close(self):
        for reporter in self.reporters:
            reporter.close()
