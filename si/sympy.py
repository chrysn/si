from __future__ import division
from __future__ import absolute_import
import si
import sympy

def nonint(s):
    if "+-" in s:
            s = s[:s.index("+-")]
    if "/" in s:
        s = s.split("/",1)
        return sympy.sympify(s[0])/sympy.sympify(s[1])
    else:
        return sympy.sympify(s)
si.nonint = nonint
def truediv(a,b):
    return sympy.sympify(a)/sympy.sympify(b)
def pow(a,b):
    return sympy.sympify(a)**sympy.sympify(b)
