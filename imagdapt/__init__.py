""" A module providing tools to extract parts of an image.


Overview:
---------

    This module defines a `Point` object and `Grid` object made of an
    array of points.

    Once a `Grid` has been instantiated, it can be bound to a
    `PIL.Image` while also providing a destination size. After that,
    various extraction tools can be used to extract the part of the
    image defined by the grid.

    The resulting image is a flatten perspective of the part, mapped to
    a rectangle according to the grid, of size the destination size
    provided when binding the grid.

    For a result example, use the command `python -m imagdapt test`.
    For a code example, see in `__main__.py`.

Extraction modes:
-----------------

    This module defines 3 extraction strategies:

        1. `MODE_QUAD` - quadrilateral extraction:
            only uses the four corners of the grid; the shape hence
            defined is a quadrilateral

        2. `MODE_LINE` - linear extraction:
            proceed to extract each cell of the grid as quadrilaterals;
            in the result, all cells takes up the same size

        3. `MODE_POLY` - polynomial extraction:
            TODO: extracts using continuous functions across the grid
            to avoid the slicing that occur with the linear mode

Hum:
----

        .-----------------------------------------------------.
        |                                                     |
        |                                                     |
        |                             __..---^B               |
        |                  A.----^"'"`        |               |
        |                   \\          =)     |               |
        |                    \\                |               |
        |                     D----...__      |               |
        |                               `'"^--C               |
        '-----------------------------------------------------'

                A---------------------------------B
                |                                 |
                |                _   \\            |
                |                _    |           |
                |                    /            |
                |                                 |
                D---------------------------------C
"""

from time import time_ns

def log(tag, *elm):
    """ logs data to stdout

        format is: `"[{tag}]: {elm}\\n"` with elements of `elm`
        separated by spaces
    """
    print("[" + tag + "]:", *elm)

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
