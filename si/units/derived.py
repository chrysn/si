# encoding: utf8
"""Units derived from SI base units."""
from si.units.base import *
from si import math, nonint

_register = ModuleSIRegister(locals())
r = _register.register # less writing

# as by si definition (table 3)
r(m/m,"rad","radian","plane angle", map="never") # FIXME: find satisfactory solution
r(m**2/m**2,"sr","steradian","solid angle", map="never")
r(s**-1,"Hz","herz","frequency", prefixes=list("YZEPTGMk"))
r(kg*m/s/s,"N","newton","force", prefixes=True)
r(N/m**2,"Pa","pascal","pressure, stress", prefixes=True)
r(N*m,"J","joules","energy, work, amount of heat", prefixes=True)
r(J/s,"W","watt","power, radiant flux", prefixes=True)
r(s*A,"C","coulomb","electric charge, amount of electricity", prefixes=True)
r(W/A,"V","volt","electrical porential difference, electromotive force", prefixes=True)
r(C/V,"F","farad","capacitence", prefixes=True)
r(V/A,[u"Ω",u"Ω"],"ohm","electric resistance", prefixes=True)
r(A/V,"S","siemens","electric conductance", prefixes=True)
r(V*s,"Wb","weber","magnetic flux", prefixes=True)
r(Wb/m/m,"T","tesla","magnetic flux density", prefixes=True)
r(Wb/A,"H","henry","inductance", prefixes=True)
# degree Celsius causes much headache
r(cd*sr,"lm","lumen","luminous flux", map="never")
r(lm/m**2,"lx","lux","illuminance", map="never")
r(s**-1,"Bq","bequerel","activity referred to a radionuclide")
r(J/kg,"Gy","gray","absorbed dose, specific energy (imparted), kerma")
r(J/kg,"Sv","sievert","dose equivalent, ambient dose equivalent, directional dose equivalent, personal dose equivalent")
r(mol/s,"kat","katal","catalytic activity")


# accepted non-si units (by si definition) (table 6)
r(60*s,"min","minute")
r(60*min,"h","hour")
r(24*h,"d","day")
r(nonint("1/180")*math.pi*rad,u"°","degree","plane angle", map="never")
r(degree/60,u"′","minute","plane angle", map="never") # this does not conflict with 1/60 hour because minute (time) is abbreviated "min" (which can be used) and minute (angle) is abbreviated u"..." which can not be used, so the long name is used. FIXME: this will not be obvious to users.
r(minute/60,u"″","second","plane angle", map="never") # same goes here
map(10**4*m**2,"ha","hectare","area", map="never")
map(nonint("1/10")**3*m**3,["l","L"],"litre","volume", prefixes=True, map="always")
map(10**3*kg,"t","tonne","mass", map="never")

# for use with prefixes or general usability
map(m**2,"m2","square metre", prefixes="m2", map="never")
map(m**3,"m3","cubic metre", prefixes="m3", map="never")

del r # clean up
