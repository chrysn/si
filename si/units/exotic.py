# encoding: utf8
"""Funny units."""
from si.math import nonint
from si.units.derived import *

_register = ModuleSIRegister(locals())
_register.prefix()
r = _register.register # less writing

r(m*nonint("3.08567758128")*10**16, "pc", "parsec", "distance from the Earth to a star that has a parallax of 1 arcsecond", prefixes = True, map="never")

r(h*24*14, [], "fortnight", prefixes = True, map="never")

del r, nonint # clean up
