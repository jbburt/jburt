"""
Utilities related to logging and IO.
"""

import sys


class Tee(object):
    """
    https://stackoverflow.com/a/616686
    """

    def __init__(self, fname, mode="w"):
        self.file = open(fname, mode)
        self.stdout = sys.stdout
        sys.stdout = self

    def __del__(self):
        sys.stdout = self.stdout
        self.file.close()

    def write(self, data):
        self.file.write(data)
        self.stdout.write(data)

    def flush(self):
        self.file.flush()


class StreamToLogger(object):
    """
    Psuedo file-like stream object that redirects writes to a logger instance.
    """

    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
        self.linebuf = ""

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.level, line.rstrip())

    def flush(self):
        pass
