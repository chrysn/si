# encoding: utf8
"""Units derived from SI base units."""
from si.units.base import *
from si.math import pow, nonint, pi

_register = ModuleSIRegister(locals())
r = _register.register # less writing

# as by si definition (table 3)
r(m/m,"rad","radian","SI unit of plane angle", map="never") # FIXME: find satisfactory solution
r(m**2/m**2,"sr","steradian","SI unit of solid angle", map="never")
r(1/s,"Hz","herz","SI unit of frequency", prefixes=list("YZEPTGMk"), map="always")
r(kg*m/s/s,"N","newton","SI unit of force", prefixes=True, map="always")
r(N/m**2,"Pa","pascal","SI unit of pressure, stress", prefixes=True, map="always")
r(N*m,"J","joules","SI unit of energy, work, amount of heat", prefixes=True, map="always")
r(J/s,"W","watt","SI unit of power, radiant flux", prefixes=True, map="always")
r(s*A,"C","coulomb","SI unit of electric charge, amount of electricity", prefixes=True, map="always")
r(W/A,"V","volt","SI unit of electrical porential difference, electromotive force", prefixes=True, map="always")
r(C/V,"F","farad","SI unit of capacitance", prefixes=True, map="always")
r(V/A,[u"Ω",u"Ω"],"ohm","SI unit of electric resistance", prefixes=True, map="always")
r(A/V,"S","siemens","SI unit of electric conductance", prefixes=True, map="always")
r(V*s,"Wb","weber","SI unit of magnetic flux", prefixes=True, map="always")
r(Wb/m/m,"T","tesla","SI unit of magnetic flux density", prefixes=True, map="always")
r(Wb/A,"H","henry","SI unit of inductance", prefixes=True)
# degree Celsius causes much headache
r(cd*sr,"lm","lumen","SI unit of luminous flux", map="never")
r(lm/m**2,"lx","lux","SI unit of illuminance", map="never")
r(1/s,"Bq","bequerel","SI unit of activity referred to a radionuclide", map="never")
r(J/kg,"Gy","gray","SI unit of absorbed dose, specific energy (imparted), kerma")
r(J/kg,"Sv","sievert","SI unit of dose equivalent, ambient dose equivalent, directional dose equivalent, personal dose equivalent")
r(mol/s,"kat","katal","SI unit of catalytic activity")


# accepted non-si units (by si definition) (table 6)
r(60*s,"min","minute","SI accepted Non-SI unit of time")
r(60*min,"h","hour","SI accepted Non-SI unit of time")
r(24*h,"d","day","SI accepted Non-SI unit of time")
r(nonint("1/180")*pi*rad,u"°","degree","SI accepted Non-SI unit of plane angle", map="never")
r(degree/60,u"′","minute","SI accepted Non-SI unit of plane angle", map="never") # this does not conflict with 1/60 hour because minute (time) is abbreviated "min" (which can be used) and minute (angle) is abbreviated u"..." which can not be used, so the long name is used. FIXME: this will not be obvious to users.
r(minute/60,u"″","second","SI accepted Non-SI unit of plane angle", map="never") # same goes here
r(10**4*m**2,"ha","hectare","SI accepted Non-SI unit of area", map="never")
r(m**3*pow(10,-3),["L","l"],"litre","SI accepted Non-SI unit of volume", prefixes=True, map="always")
r(10**3*kg,"t","tonne","SI accepted Non-SI unit of mass", map="never")

# for use with prefixes or general usability
r(m**2,"m2","square metre", prefixes="m2", map="never")
r(m**3,"m3","cubic metre", prefixes="m3", map="never")

del r, pi, nonint, pow # clean up
