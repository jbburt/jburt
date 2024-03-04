# ~/.ipython/profile_default/startup/startup.py
import IPython

if 'IPython' in globals():
    ip = IPython.get_ipython()
    ip.run_line_magic('load_ext', 'autoreload')
    ip.run_line_magic('autoreload', '2')

import builtins


def print(*args, **kwargs):
    timestamp = (
        builtins.__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    prefix = f"\n[{timestamp}] "
    suffix = "\n\n"
    builtins.print(prefix, *args, **kwargs, end=suffix)
