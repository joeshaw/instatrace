# Copyright (c) 2011 litl, LLC

import os
import unittest

from contextlib import contextmanager

from instatrace import tracer
from instatrace.reporters.file import FileReporter


class TestReporter(object):
    def __init__(self):
        self.last_trace = None

    def trace(self, stat, value, user_data):
        self.last_trace = dict(stat=stat,
                               value=value,
                               user_data=user_data)

    def reset(self):
        self.last_trace = None


class TracerTests(unittest.TestCase):
    def assert_last_value(self, reporter, stat, value, user_data):
        self.assertNotEqual(reporter.last_trace, None)
        self.assertEquals(reporter.last_trace['stat'], stat)
        self.assertEquals(reporter.last_trace['value'], value)
        self.assertEquals(reporter.last_trace['user_data'], user_data)

    def assert_last_value_less_than(self, reporter, stat, value, user_data,
                                    tolerance):
        self.assertNotEqual(reporter.last_trace, None)
        self.assertEquals(reporter.last_trace['stat'], stat)
        self.assertEquals(reporter.last_trace['user_data'], user_data)

        if abs(value - reporter.last_trace['value']) > tolerance:
            self.fail("value %s exceeds tolerance of +/-%s of %s"
                      % (reporter.last_trace['value'], tolerance, value))

    @contextmanager
    def trace_context(self, reporter):
        yield
        reporter.reset()

    def test_tracer(self):
        self.assertEquals(tracer.reporters, [])

        reporter = TestReporter()
        tracer.add_reporter(reporter)

        self.assertEquals(len(tracer.reporters), 1)
        self.assertEquals(tracer.reporters[0], reporter)

        self.assertEquals(reporter.last_trace, None)

        stat = "test.tracer.value"
        value = 5580

        with self.trace_context(reporter):
            tracer.trace(stat, value)
            self.assert_last_value(reporter, stat, value, None)

        user_data = { "foo": 100, "bar baz quux": "hal hal hal" }
        with self.trace_context(reporter):
            tracer.trace(stat, value, user_data)
            self.assert_last_value(reporter, stat, value, user_data)

        user_data = {}
        with self.trace_context(reporter):
            start = tracer.now_us()
            with tracer.trace_us(stat, user_data):
                user_data['foo'] = 99
            end = tracer.now_us()
            self.assert_last_value_less_than(reporter, stat, end - start,
                                             user_data, tolerance=100)

        with self.trace_context(reporter):
            start = tracer.now_ms()
            with tracer.trace_ms([stat]):
                pass
            end = tracer.now_ms()
            self.assert_last_value_less_than(reporter, stat, end - start,
                                             None, tolerance=10)

    def test_file_reporter(self):
        filename = '/tmp/test-file-reporter.txt'
        reporter = FileReporter(filename)
        reporter.trace("test.reporter.stat", 100,
                       {'foo': 'bar', 'hal hal hal': 'hal' })
        reporter.close()

        with open(filename, 'r') as f:
            contents = f.read()

        expected_contents = "test.reporter.stat 100 {'foo': 'bar', 'hal hal hal': 'hal'}\n"

        self.assertEquals(contents, expected_contents)
        os.unlink(filename)
