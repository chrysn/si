# encoding: utf8
"""Funny units."""
from si.units.derived import *
from si.units.prefixed import *
from si import prefixes as _prefixes

parsec=3.08567758128*10**16*m
attoparsec=_prefixes.atto*parsec

fortnight=h*24*14
microfortnight=_prefixes.micro*fortnight
