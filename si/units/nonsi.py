# encoding: utf8
"""Units accepted for SI use"""
from si.math import pow, nonint, pi
from si.units.derived import *
from si import prefixes as _prefixes
_register = ModuleSIRegister(locals())
r = _register.register # less writing

# by si description (table 8)
r(10**5*Pa,"bar","bar","old unit of pressure", prefixes=True)
r(Pa*nonint("133.322"),"mmHg","millimetre of mercury","old unit of pressure", map="never")
r(m*pow(10,-10),[u"Å",u"Å"],[u"ångström","angstrom"],"unit of distance used by x-ray crystallographers and structural chemists")
r(1852*m,"M","nautical mile","unit of distance used in navigation", map="never")
r(m2*pow(10,-28),"b","barn","unit of area used in nuclear physics", map="never")
r(M/h,"kt","knot","unit of speed derived from nautical mile", map="never")
# neper, bel and decibel not implemented lacking understanding of the problems (and/or time)

# CGS system (table 9)
r(m*pow(10,-2),"cm","centimetre","CGS unit of distance", map="never") # CGS is based on cm, adding it here
r(J*pow(10,-7),"erg","erg","CGS unit of energy", map="never")
r(N*pow(10,-5),"dyn","dyne","CGS unit of force", map="never")
r(dyn*s/cm/cm,"P","poise","CGS unit of dynamic viscosity", map="never")
r(cm*cm/s,"St","stokes","CGS unit of kinematic viscosity", map="never")
r(cd/cm/cm,"sb","stilb","CGS unit of luminance", map="never")
r(cd*sr/cm/cm,"ph","phot","CGS unit of illuminance", map="never")
r(cm/s**2,"Gal","gal","CGS unit of acceleration", map="never")
r(Wb*pow(10,-8),"Mx","CGS unit of maxwell","magnetic flux", map="never")
r(Mx/cm/cm,"G","gauss","CGS unit of magnetic flux density", map="never")
r(A/m*(pow(10,3)/(4*pi)),"Oe",u"œrsted","CGS unit of magnetic field", map="never")

del r, pow, nonint, pi
