from __future__ import division
from __future__ import absolute_import

from math import * # provide everything the normal math module provides

def nonint(s):
	"""SI.nonint is used by prefixes and units to allow for flexible handling of non-integer numbers (integers are assumed to work in all situations).

	Passed s will roughly fit "$DECIMAL(/$DECIMAL)?(+-$DECIMAL(/$DECIMAL))?"; you get the idea. +- indicates standard uncertainity, just in case some system cares, and can be discarded by most implementations."""
	if "+-" in s:
		assert len(s) == 2*s.index("+-")+2, "I think you got the standard uncertainities wrong. Fix me if I'm wrong."
		s = s[:s.index("+-")]
	if "/" in s:
		s = s.split("/",1)
		return truediv(float(s[0]),float(s[1]))
	else:
		return float(s)
def truediv(a,b):
	"""Return a/b, both of which can be int, whatever is returned by nonint, or basically anything else."""
	if a/b == a//b:
		return a//b
	else:
		return a/b
def simplest_form(value):
	"""Return something that has a simple string representation. Here, this means converting floats to integers if possible without loss of data."""
	if value == int(value):
		return int(value)
	return value
