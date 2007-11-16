"""Dummy module to load a default simaths module from mathmodules"""

from .mathmodules import choose
choose('python', locals()) # no command should be below this line because choose() will affect this module's locals
