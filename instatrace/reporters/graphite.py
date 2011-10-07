# Copyright (c) 2011 litl, LLC

import socket
import time

class GraphiteReporter(object):
    def __init__(self, host, port, throw_errors=False):
        self.host = host
        self.port = port
        self.throw_errors = throw_errors

        self.sock = None

    def connect(self):
        if self.sock is not None:
            return

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((self.host, self.port))
            self.sock = sock
        except socket.error:
            if self.throw_errors:
                raise

    def disconnect(self):
        if self.sock is None:
            return

        try:
            self.sock.close()
        except socket.error:
            pass
        finally:
            self.sock = None

    def send(self, msg, tries=2):
        while tries > 0:
            tries -= 1

            if not self.sock:
                self.connect()

            if not self.sock:
                # reconnection failed silently
                continue

            try:
                self.sock.sendall(msg)
                break
            except socket.error:
                self.disconnect()

                if tries == 0 and self.throw_errors:
                    raise

    def trace(self, stat, value, user_data):
        # user_data is ignored in the graphite reporter
        format = "%s %s %d\n"

        self.send(format % (stat, value, time.time()))

    def close(self):
        self.disconnect()
