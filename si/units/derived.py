# encoding: utf8
"""Units derived from SI base units."""
from si.units.base import *

# as by si definition (table 3)
rad = m/m
sr = m**2/m**2
Hz = s**-1
N = kg*m/s/s
Pa = N/m/m
J = N*m
W = J/s
C = s*A
V = W/A
F = C/V
Ohm = V/A # would have to be Ω or Ω
S = A/V
Wb = V*s
T = Wb/m/m
H = Wb/A
# degree Celsius causes much headache
lm = cd*sr
lx = lm/m**2
Bq = s**-1
Gy = J/kg
Sv = J/kg
kat = mol/s


# accepted non-si units (by si definition) (table 6)
min = 60*s
h = 60*min
d = 24*h
# angles left out; should be °, ′, ″
ha = 10**4*m**2
l = 10**-3*m**3
t = 10**3*kg

# for use with prefixes or general usability
g = kg/1000
m2 = m**2
m3 = m**3
