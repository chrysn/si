# encoding: utf8
"""Units accepted for SI use"""
from si import math, nonint
from si.units.derived import *
from si import prefixes as _prefixes
_register = ModuleSIRegister(locals())
r = _register.register # less writing

# by si description (table 8)
r(10**5*Pa,"bar","bar","pressure", prefixes=True)
r(nonint("133.322")*Pa,"mmHg","millimetre of mercury", map="never")
r(nonint("1/10")**10*m,[u"Å",u"Å"],[u"ångström","angstrom"],"distance")
r(1852*m,"M","nautical mile","distance", map="never")
r(nonint("1/10")**28*m2,"b","barn","area", map="never")
r(nonint("1852/3600")*m/s,"kt","knot","speed", map="never")
# neper, bel and decibel not implemented lacking understanding of the problems (and/or time)

# CGS system (table 9)
r(nonint("1/100")*m,"cm","centimetre","distance", map="never") # CGS is based on cm, adding it here
r(nonint("1/10")**7*J,"erg","erg","energy", map="never")
r(nonint("1/10")**5*N,"dyn","dyne","force", map="never")
r(dyn*s/cm/cm,"P","poise","dynamic viscosity", map="never")
r(cm*cm/s,"St","stokes","kinematic viscosity", map="never")
r(cd/cm/cm,"sb","stilb","luminance", map="never")
r(cd*sr/cm/cm,"ph","phot","illuminance", map="never")
r(cm/s**2,"Gal","gal","acceleration", map="never")
r(nonint("1/10")**8*Wb,"Mx","maxwell","magnetic flux", map="never")
r(Mx/cm/cm,"G","gauss","magnetic flux density", map="never")
r((10**3/(4*math.pi))*A/m,"Oe",u"œrsted","magnetic field", map="never")

del r
