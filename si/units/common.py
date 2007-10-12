from si.units.base import *
from si.units.derived import *
from si.units.nonsi import *
from si.units.other import *

from si import ModuleSIRegister
for register in ModuleSIRegister.loadedmodules:
    register.prefix()
del register, ModuleSIRegister

# now pull prefixed units. not beautyful, but works.
from si.units.base import *
from si.units.derived import *
from si.units.nonsi import *
from si.units.other import *
