"""SI base units."""
from si import SI
from si.register import ModuleSIRegister
_register = ModuleSIRegister(locals())
r = _register.register # less writing

# as by si definition

r(SI((1,(1,0,0,0,0,0,0))),"m","metre", "SI base unit of length", prefixes=True, map="always")
r(SI((1,(0,1,0,0,0,0,0))),"kg","kilogram", "SI base unit of mass", prefixes="kg", map="always")
r(SI((1,(0,0,1,0,0,0,0))),"s","second", "SI base unit of time", prefixes=True, map="always")
r(SI((1,(0,0,0,1,0,0,0))),"A","ampere", "SI base unit of electric current", prefixes=True, map="always")
r(SI((1,(0,0,0,0,1,0,0))),"K","kelvin", "SI base unit of thermodynamic temperature", prefixes=True, map="always")
r(SI((1,(0,0,0,0,0,1,0))),"mol","mole", "SI base unit of amount of substance", prefixes=True, map="always")
r(SI((1,(0,0,0,0,0,0,1))),"cd","candela", "SI base unit of luminous intensity", prefixes=True, map="always")

del r # clean up
