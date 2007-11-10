# encoding: utf8
"""Experimental and other useful units."""
from si.units.derived import *

from si.math import pow, nonint

_register = ModuleSIRegister(locals())
r = _register.register # less writing

# non-si units whose values in si units must be obtained experimentally, by si description (table 7)
r(J*pow(10,-19)*nonint("1.60217653+-0.00000014"), "eV", "electronvolt", "energy", prefixes=True)
r(kg*pow(10,-25)*nonint("1.66053886+-0.00000028"), ["u","Da"], ["Dalton", "Unit"], "mass")
r(m*pow(10,11)*nonint("1.49597870691+-0.00000000006"),"ua","astronomical unit","length")
# natural units
r(299792458*m/s,["c",u"c₀"],"speed of light in vacuum","n.u. of speed")
r(J*s*pow(10,-34)*nonint("1.05457168+-0.00000018"), ["h__stroke",u"₀"], "reduced Planck constant", "n.u. of action")
r(kg*pow(10,-31)*nonint("9.1093826+-0.0000016"), "m_e", "electron mass", "n.u. of mass") # FIXME: make m_e know it is LaTeX notation
# atomic units
r(C*pow(10,-19)*nonint("1.60217653+-0.00000014"), "e", "elementary charge", "a.u. of charge")
r(m*pow(10,-10)*nonint("0.5291772108+-0.0000000018"), ["m_0", u"m₀"], "bohr", "a.u. of length, Bohr radius")
r(J*pow(10,-18)*nonint("4.35974417+-0.00000075"), "E_h", "hartree", "a.u. of energy, Hartree energy")

# other
r(8766*h*c, "ly", "lightyear", "distance light covers in vacuum in one year") # as recommended by the iau http://www.iau.org/Units.234.0.html

del r, pow, nonint
