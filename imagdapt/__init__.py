"""
        A------------------B
        |                  |
        |                  |
        |                  |
        D------------------C
"""

from time import time_ns

def log(tag, *text):
    """ logs to stdout

        format is: `[{tag}]: {text}

        elements are separated by spaces

        ends with a new line
    """
    print("[" + tag + "]:", *text)

def time(task, result):
    """ times the given task using the built-in `time.time_ns`

        calls `task.__call__` (function call) and returns what it
        returns

        `result` should be a `dict` to hold the result of the timing;
        the following keys are sets:
         - 'time': time, in nanoseconds, it took to execute the task
         - 'begin': value from `time.time_ns` before the call
         - 'end': value from `time.time_ns` after the call
         - 'return': what is returned by the call to the `task`
    """
    assert isinstance(result, dict)

    begin = time_ns()
    r = task()
    end = time_ns()

    result['time'] = end - begin
    result['begin'] = begin
    result['end'] = end
    result['return'] = r

    return r

MODE_QUAD = -1
MODE_LINE = 2
MODE_POLY = 3

from imagdapt.extra import Util, Extractor
from imagdapt.shape import Point, Grid

__all__ = [
    'Util',
    'Point',
    'Grid',
    'MODE_QUAD',
    'MODE_LINE',
    'MODE_POLY'
]
