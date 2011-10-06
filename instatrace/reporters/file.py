# Copyright (c) 2010 Peter Teichman
# Copyright (c) 2011 litl, LLC

import datetime
import os

class FileReporter(object):
    def __init__(self, filename):
        # rotate logs if present
        if os.path.exists(filename):
            now = datetime.datetime.now()
            stamp = now.strftime("%Y-%m-%d.%H%M%S")
            os.rename(filename, "%s.%s" % (filename, stamp))

        self._fd = open(filename, "w")

    def trace(self, stat, value, user_data):
        extra = ""
        if user_data is not None:
            extra = " " + repr(user_data)

        self._fd.write("%s %d%s\n" % (stat, value, extra))

    def close(self):
        self._fd.close()
