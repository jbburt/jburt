"""
Utilities related to logging.
"""
import sys

import openai

from ._config import CACHE


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


class LLMCache:
    file = "log.jsonl"
    sep = "===================="
    prompt_key = "prompt"
    answer_key = "answer"

    def __init__(self, parts, file: str = file):
        self.file = file
        self.logpath = CACHE.joinpath(*parts) / self.file
        self.logpath.parent.mkdir(exist_ok=True, parents=True)

    def __call__(
        self,
        prompt: str,
        response: openai.types.chat.chat_completion.ChatCompletion,
        debug: bool = False,
    ):
        with open(self.logpath, "a") as f:
            write = print if debug else f.write
            d = {
                self.prompt_key: prompt,
                self.answer_key: response.choices[0].message.content,
            }
            write(d)
            write(self.sep)
