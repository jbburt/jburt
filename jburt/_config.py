import os
import pathlib

__all__ = ["ROOT", "CACHE"]

ROOT = pathlib.Path(os.environ["HOME"])
CACHE = ROOT / ".cache"
CACHE.mkdir(exist_ok=True)
