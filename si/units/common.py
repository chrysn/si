from si.units.base import *
from si.units.derived import *
from si.units.nonsi import *
from si.units.other import *

from si.register import ModuleSIRegister
for register in ModuleSIRegister.loadedmodules:
    register.prefix()
del register, ModuleSIRegister

# now pull prefixed units. not beautiful, but works.
from si.units.base import *
from si.units.derived import *
from si.units.nonsi import *
from si.units.other import *
