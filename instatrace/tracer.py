# Copyright (c) 2010 Peter Teichman
# Copyright (c) 2011 litl, LLC

import time
import types

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
    def trace_us(self, stats, user_data=None):
        if not type(stats) in (types.ListType, types.TupleType):
            stats = [stats]
        start = self.now_us()
        yield
        end = self.now_us()
        diff = end - start
        for stat in stats:
            self.trace(stat, diff, user_data)

    @contextmanager
    def trace_ms(self, stats, user_data=None):
        if not type(stats) in (types.ListType, types.TupleType):
            stats = [stats]
        start = self.now_ms()
        yield
        end = self.now_ms()
        diff = end - start
        for stat in stats:
            self.trace(stat, diff, user_data)

    def close(self):
        for reporter in self.reporters:
            reporter.close()
