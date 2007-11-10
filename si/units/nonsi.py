# encoding: utf8
"""Units accepted for SI use"""
from si.math import pow, nonint, pi
from si.units.derived import *
from si import prefixes as _prefixes
_register = ModuleSIRegister(locals())
r = _register.register # less writing

# by si description (table 8)
r(10**5*Pa,"bar","bar","pressure", prefixes=True)
r(Pa*nonint("133.322"),"mmHg","millimetre of mercury", map="never")
r(m*pow(10,-10),[u"Å",u"Å"],[u"ångström","angstrom"],"distance")
r(1852*m,"M","nautical mile","distance", map="never")
r(m2*pow(10,-28),"b","barn","area", map="never")
r(m/s*nonint("1852/3600"),"kt","knot","speed", map="never")
# neper, bel and decibel not implemented lacking understanding of the problems (and/or time)

# CGS system (table 9)
r(m*pow(10,-2),"cm","centimetre","distance", map="never") # CGS is based on cm, adding it here
r(J*pow(10,-7),"erg","erg","energy", map="never")
r(N*pow(10,-5),"dyn","dyne","force", map="never")
r(dyn*s/cm/cm,"P","poise","dynamic viscosity", map="never")
r(cm*cm/s,"St","stokes","kinematic viscosity", map="never")
r(cd/cm/cm,"sb","stilb","luminance", map="never")
r(cd*sr/cm/cm,"ph","phot","illuminance", map="never")
r(cm/s**2,"Gal","gal","acceleration", map="never")
r(Wb*pow(10,-8),"Mx","maxwell","magnetic flux", map="never")
r(Mx/cm/cm,"G","gauss","magnetic flux density", map="never")
r(A/m*(pow(10,3)/(4*pi)),"Oe",u"œrsted","magnetic field", map="never")

del r, pow, nonint, pi
