"""Experimental and other useful units."""
from si.units.derived import *
from si.units.prefixed import *

# non-si units whose values in si units must be obtained experimentally, by si description (table 7)
# (xx) is the standard uncertainity of the last digits, units i would not recognize immediately are commented with name
eV = 1.60217653*10**-19*J # (14)
Da = 1.66053886*10**-25*kg # (28); Dalton
u = Da
ua = 1.49597870691*10**11*m # (6); astronomical unit
# natural units
c = 299792458*m/s # by definition
h__stroke = 1.05457168*10**-34*J*s # (18)
m_e = 9.1093826*10**-31*kg # (16); mass of an electron
# atomic units
e = 1.60217653*10**-19*C # (14)
a_0 = 0.5291772108*10**-10*m # (18); bohr radius
E_h = 4.35974417*10**-18*J # (75); hartree energy

# other
ly = 356.25*24*h*c # light year as recommended by the iau http://www.iau.org/Units.234.0.html
