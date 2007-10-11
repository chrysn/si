# encoding: utf8
"""Units accepted for SI use"""
from si.units.derived import *
from si import prefixes as _prefixes
import math as _math

# by si description (table 8)
bar = 10**5*Pa
mmHg = 133.322*Pa # roughly
Angrstrom = 10**-10*m # should be Å or Å
M = 1852*m # nautical mile
b = 10**-28*m2 # barn
kn = 1852/3600*m/s # knot
# neper, bel and decibel not implemented lacking understanding of the problems (and/or time)

# CGS system
cm = m/100 # CGS is based on cm, adding it here
erg = 10**-7*J
dyn = 10**-5*N
P = dyn*s/cm/cm
St = cm*cm/s
sb = cd/cm/cm
ph = cd*sr/cm/cm
Gal = cm/s**2
Mx = 10**-8*Wb
G = Mx/cm/cm
Oe = (10**3/(4*_math.pi))*A/m
