"""
Utilities related to logging and IO.
"""
import json
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


class QACache:
    """
    A cache for QA data.

    todo: inherit from generic TextIOBase (or something more appropriate)
    """

    fname = "log.jsonl"
    system_key = "system"
    prompt_key = "prompt"
    answer_key = "answer"

    @staticmethod
    def to_json(system: str, prompt: str, answer: str) -> dict:
        return {
            QACache.system_key: system,
            QACache.prompt_key: prompt,
            QACache.answer_key: answer,
        }

    def __init__(self, parts, file: str = fname):
        self.fname = file
        self.parts = parts
        self.path = CACHE.joinpath(*parts) / self.fname
        self.path.parent.mkdir(exist_ok=True, parents=True)

    def __call__(self, *args, **kwargs):
        return self.append(*args, **kwargs)

    def append(
        self,
        prompt: str,
        response: openai.types.chat.chat_completion.ChatCompletion,
        system: str = None,
        debug: bool = False,
    ) -> dict:
        """
        Append to the log.

        Args:
            prompt (str): The prompt.
            response (openai.types.chat.chat_completion.ChatCompletion): The response.
            system (str): The system prompt.
            debug (bool): Whether to print to stdout instead of the log file.

        Returns:
            dict: JSON object with system prompt, user prompt, and (str) response.
        """
        json = self.to_json(system, prompt, response.choices[0].message.content)
        with open(self.path, "a") as f:
            write = print if debug else f.write
            write(str(json) + "\n")
        return json
