"""SymPy glue code.

>>> import sys
>>> for m in sys.modules.keys(): # as this is also run from doctest, this loop cleans up before running sympy si tests
...     if m.startswith('si.') or m=='si':
...         del sys.modules[m]
>>> import si.mathmodules
>>> si.mathmodules.choose('sympy')
>>> from si.common import *
>>> print Oe
250/pi A/m

And now for something completely different:
>>> import doctest
>>> doctest.testmod(si) # doctest: +ELLIPSIS
TestResults(failed=0, ...)
>>> doctest.testmod(si.register) # doctest: +ELLIPSIS
TestResults(failed=0, ...)
"""
from __future__ import division
from __future__ import absolute_import
import si

from sympy import *

def nonint(s):
    if "+-" in s:
            s = s[:s.index("+-")]
    if "/" in s:
        s = s.split("/",1)
        return sympify(s[0])/sympify(s[1])
    else:
        return sympify(s)
def truediv(a,b):
    return sympify(a)/sympify(b)
def pow(a,b):
    return sympify(a)**sympify(b)
def simplest_form(value): # there is no float quirx here.
    return value
