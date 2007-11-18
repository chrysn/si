# encoding: utf-8
"""Module for (annotated) unit housekeeping; see ``ModuleSIRegister``."""
from __future__ import division
import string
import si.math

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

class SIUnit(object):
	"""Container to store meta information about an ``SI`` quantity that is a unit. Stores prefix preferences, name, symbol, description, and display preferences. Listed via ``ModuleSIRegister``s, which in turn have their own mechanism to be listed.
	
	Should in most cases be constructed via the ``ModuleSIRegister``s' ``register()`` function."""

	all_prefixes = list('YZEPTGMkhdcmunpfazy') + ["da"]
	def __init__(self, unit, symbol, name, description, prefixes, map):
		"""See ``ModuleSIRegister.register`` for details."""
		self.unit, self.symbol, self.name, self.description, self.prefixes, self.map = unit, symbol, name, description, prefixes, map
	
	@staticmethod
	def _istex(s):
		return s.startswith("$") and s.endswith("$")

	def get_prefixed(self):
		"""Return a list of 2-tuples with prefixed python-usable name versions and the corresponding unit value."""
		import si.prefixes
		if not self.prefixes:
			return []
		elif self.prefixes == "kg": # magic handling of kg, see section 3.2 of the brochure
			assert self.name == ["kilogram"], "Prefixing kg style only makes sense for kg. Fix me if I'm wrong."
			g = self.unit / 1000
			r = [("g", g)]
			for p in self.all_prefixes:
				if p != "k":
					r.append((p+"g", g * getattr(si.prefixes, p)))
			return r
		elif self.prefixes == "m2": # magic handling to have a convenient way of writing square mm as mm2 instead of mm**2 (which is != milli*m**2, as it would happen if regularly prefixing m2)
			assert self.name == ["square metre"], "Prefixing m2 style only makes sense for m2. Fix me if I'm wrong."
			r = []
			for p in self.all_prefixes:
				r.append((p+"m2", self.unit * getattr(si.prefixes, p)**2))
			return r
		elif self.prefixes == "m3": # as with m2
			assert self.name == ["cubic metre"], "Prefixing m3 style only makes sense for m3. Fix me if I'm wrong."
			r = []
			for p in self.all_prefixes:
				r.append((p+"m3", self.unit * getattr(si.prefixes, p)**3))
			return r
		elif self.prefixes == True:
			prefixes = self.all_prefixes
		else:
			prefixes = self.prefixes

		r = []
		for n in self.get_python_names():
			for p in prefixes:
				r.append((p+n, self.unit * getattr(si.prefixes, p)))
		return r

	@staticmethod
	def _valid_python_name(s):
		return len([l for l in string.letters+"_" if s.startswith(l)]) and not len([l for l in s if l not in string.letters+string.digits+"_"])

	def get_python_names(self):
		"""Yield at least one name that can be used to address the unit in python. First (long) name will be used if all (short) prefixes are unusable as python identifiers."""
		setone = False
		for n in self.symbol:
			if self._valid_python_name(n):
				yield n
				setone = True
		if not setone:
			for n in self.name:
				if self._valid_python_name(n):
					yield n
					break
			else:
				raise Exception("Can not register unit name: no prefix or name appropriate.")

	def preferred_symbol(self, allow_unicode):
		if allow_unicode:
			for s in self.symbol + self.name:
				if not self._istex(s):
					return s
			raise Exception, "No unicode symbol available."
		else:
			for s in self.symbol + self.name:
				if not isinstance(s, unicode) and not self._istex(s):
					return s
			raise Exception, "No ascii symbol available."
	
	def tex(self):
		"""Return a symbol which can be used in TeX math mode."""
		for s in self.symbol:
			if self._istex(s):
				return s[1:-1]
		return self.preferred_symbol(False)

	def __repr__(self):
		return "<SIUnit: %r (%r)>"%(self.name[0],self.symbol[0])

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
	
	>>> from si.common import *
	>>> from si.register import search_prefixed
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

	result = 1

	decomp = decomposition_from_pure_string(unit)
	for ((prefix,unit),power) in decomp.iteritems():
		result = result * (unit.unit*prefix)**power

	result = result * si.math.nonint(number)

	return result

def decomposition_from_pure_string(s):
	result = {}
	pospow = True

	while s:
		if s.startswith("*") or s.startswith(" "):
			s = s[1:]
			continue

		if s.startswith("/"):
			if pospow == False: raise Exception,"Consecutive slashes don't make sense."
			pospow = False
			s = s[1:]
			continue

		if s.startswith("("):
			end = s.find(")")
			inside = decomposition_from_pure_string(s[1:end])
			if not pospow:
				inside = dict((k,-v) for (k,v) in inside.iteritems())
			for k,v in inside.iteritems():
				result[k] = result.get(k,0) + v

			s = s[end+1:]
			pospow = True
			continue

		for x in range(len(s),0,-1):
			try:
				thisunit = search_prefixed(s[:x])
			except:
				continue

			s = s[x:]
			if s.startswith("^"):
				power = int(s[1]) # FIXME if someone complains. will raise an exception if my assertion was wrong.
				s=s[2:]
			else:
				power = 1
			if not pospow:
				power = power * (-1)

			result[thisunit] = result.get(thisunit, 0) + power
			pospow = True
			break
		else:
			raise Exception("Can not convert to unit: %s"%s)
	
	return result

