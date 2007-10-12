# encoding: utf8
"""Funny units."""
from si import math, nonint
from si.units.derived import *
from si import prefixes as _prefixes

_register = ModuleSIRegister(locals())
_register.prefix()
r = _register.register # less writing

r(nonint("3.08567758128")*10**16*m, "pc", "parsec", "distance from the Earth to a star that has a parallax of 1 arcsecond", prefixes = True, map="never")

r(h*24*14, [], "fortnight", prefixes = True, map="never")

del r # clean up
