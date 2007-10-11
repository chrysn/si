# encoding: utf8
"""Prefixed units, mostly from base and derived units."""
from si import prefixes
import si.units.base as u_base
import si.units.derived as u_derived
import si.units.nonsi as u_nonsi # only bar

units = {}
units['base'] = u_base.__dict__.items()
units['derived'] = u_derived.__dict__.items()
units['nonsi'] = u_nonsi.__dict__.items()
del u_base, u_derived, u_nonsi
units = dict(units['base']+units['derived']+units['nonsi'])

# prefixes chosen are quite arbitrary, based on what i know to be used, and si recommendations
_3base = list('YZEPTGMkmunpfazy')
prefixes_for_units = {
		'm':_3base+list('cd'),
		's':list('munpfazy'),
		'g':list('YZEPTGMdcmunpfazy')+['da'],
		'A':_3base,
		'K':list('munpfazy'), # others "not recommended"
		'mol':_3base,
		'cd':_3base,
		'l':list('hmunpfazy'),
		'Hz':list('YZEPTGMk'),
		'N':_3base+['da'],
		'Pa':_3base,
		'J':_3base,
		'W':_3base,
		'V':_3base,
		'C':_3base,
		'Wb':_3base,
		'Ohm':_3base,
		'H':_3base,
		'F':_3base,
		'T':_3base,
		'bar':_3base,
		}

_l = locals()
for unit,unit_prefixes in prefixes_for_units.items():
	for prefix in unit_prefixes:
		_l[prefix+unit] = units[unit] * getattr(prefixes,prefix)

for prefix in _3base:
	_l[prefix+'m2'] = _l[prefix+'m']**2
	_l[prefix+'m3'] = _l[prefix+'m']**3

del units, prefixes_for_units, unit, unit_prefixes, prefix, prefixes
