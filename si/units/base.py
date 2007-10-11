"""SI base units."""
from si import SI, ModuleSIRegister
_register = ModuleSIRegister(locals())
r = _register.register # less writing

# as by si definition

r(SI((1,(1,0,0,0,0,0,0))),"m","metre", prefixes=True, map="always")
r(SI((1,(0,1,0,0,0,0,0))),"kg","kilogram", prefixes="kg", map="always")
r(SI((1,(0,0,1,0,0,0,0))),"s","second", prefixes=True, map="always")
r(SI((1,(0,0,0,1,0,0,0))),"A","ampere", prefixes=True, map="always")
r(SI((1,(0,0,0,0,1,0,0))),"K","kelvin", prefixes=True, map="always")
r(SI((1,(0,0,0,0,0,1,0))),"mol","mole", prefixes=True, map="always")
r(SI((1,(0,0,0,0,0,0,1))),"cd","candela", prefixes=True, map="always")

del r # clean up
