# encoding: utf-8
"""Module for (annotated) unit housekeeping; see ``ModuleSIRegister``."""
from __future__ import division
import string
import si.math

from si.units import SIUnit, SICompoundUnit

class ModuleSIRegister(object):
	"""In a module, create a ``_register = ModuleSIRegister(locals())`` and add define units like ``_register.register(s**-1, "Hz", "herz", prefixes = list('YZEPTGMk'))``. Units will be made available for inclusion with import automatically, and prefixing is handled."""
	loadedmodules = [] # keep a list in the class

	def __init__(self, locals):
		self.units = []

		self.locals = locals
		self.loadedmodules.append(self)
		self._prefix = False

	@staticmethod
	def _stringlist(o):
		if isinstance(o, basestring): return [o]
		if hasattr(o, "__len__"):
			return o
		else:
			return [o]

	def register(self, unit, symbol, name, description = None, prefixes = None, map = "exact"):
		"""A wrapper around SIUnit to add a unit with symbols and names (can be string/unicode or list thereof; symbols can contain TeX representations like r"$\sigma$").
		
		prefixes is a list of SI prefix names common for that unit (or True for all, or one of ``["kg","m2","m3"]`` for magic handling). map defines if and how the unit should be used to give names to SI quantities ("always" for normal use, "exact" to match only scalar multiples of the unit, "never") """

		symbol = self._stringlist(symbol)
		name = self._stringlist(name)

		ru = SIUnit(unit, symbol, name, description, prefixes, map)
		self.units.append(ru)

		for n in ru.get_python_names():
			self.locals[n] = unit
		if self._prefix:
			for n, pu in ru.get_prefixed():
				self.locals[n] = pu
	
	def prefix(self):
		"""Include all prefixed forms of registered SI objects in the namespace and do so for all registered in future."""
		self._prefix = True

		for ru in self.units:
			for n, pu in ru.get_prefixed():
				self.locals[n] = pu


def search(q):
	"""Search loaded modules for a quantity exactly matching the search term q.
	
	>>> from si.common import *
	>>> search("u")
	<SIUnit: 'Dalton' ('u')>"""

	result = []

	for m in ModuleSIRegister.loadedmodules:
		for u in m.units:
			if q in u.symbol or q in u.name:
				result.append(u)

	if not result: raise LookupError("No matching unit.")
	assert len(result)==1, "Multiple units match that name." # should not occur with shipped modules
	return result[0]

def search_prefixed(q):
	"""Like ``search``, but strip prefixes. Return a tuple of the prefix factor and the found unit.
	
	>>> import si.common # load unit definitions
	>>> search_prefixed("Gg") # one giga-gram
	(1000000, <SIUnit: 'kilogram' ('kg')>)
	"""
	import si.prefixes
	q = q.replace(u"μ","u").replace(u"µ","u") # FIXME

	factor = 1
	stripped = q
	for p,f in vars(si.prefixes).iteritems():
		if q.startswith(p): 
			assert factor == 1, "Multiple prefixes match that name." # should not occur with shipped modules.
			factor = f
			stripped = q[len(p):]
	
	# kg needs very special handling, unfortunately.
	if stripped == "g":
		return si.math.truediv(factor,1000), search("kg")
	
	try:
		unit = search(stripped)
	except: # maybe a prefix should not have been stripped
		return (1, search(q))


	if unit.prefixes == "m2": factor = si.math.pow(factor, 2) # magic prefix handling!
	elif unit.prefixes == "m3": factor = si.math.pow(factor, 3)
	
	return factor, unit

def si_from_string(s):
	"""Convert a string to a SI quantity.
	
	>>> import si.common # load unit definitions
	>>> print si_from_string("5S/cm^2")
	50000 S/m^2
	>>> print si_from_string("5 J/(m*mol)")
	5 N/mol
	>>> print si_from_string("50 WbkA^2")
	50000000 A J
	>>> print si_from_string("kHz")
	1000 Hz

	#>>> print si_from_string("mm") # fail with sympy
	#0.001 m

	#>>> print si_from_string("degree") # fail with python maths
	#(1/180)*pi
	"""

	lastnumber = 0
	while s[lastnumber] in string.digits+"./": lastnumber+=1
	
	number, unit = s[:lastnumber].strip(),s[lastnumber:].strip()
	if not number: number = "1"

	decomp = SICompoundUnit(unit)
	result = decomp.to_unit()

	result = result * si.math.nonint(number)

	return result
