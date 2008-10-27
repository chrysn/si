# encoding: utf-8
"""Module containing the unit classes (``SIUnit`` and ``SICompoundUnit``)

Sub-modules contain concrete SI units and are managed by the ``si.register``""" #FIXME write documentation

from __future__ import division
import string

import si.register

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

	# mathematical operations on units create compound units

	def __div__(self, other):
		if isinstance(other, SIUnit): # duck typing not appropriate here; other people can implement their own mechanisms because we return NotImplemented
			return SICompoundUnit(((1, self, 1), (1, other, -1)))
		else:
			return NotImplemented
	__truediv__ = __div__

	def __rdiv__(self, other):
		if other == 1:
			return SICompoundUnit(((1, self, -1),))
		else:
			return NotImplemented
	__rtruediv__ = __rdiv__

        # BIG FIXME: implement multiplication, powers

class SICompoundUnit(tuple):
	"""Immutable formal composition of SI units. Unlike operations on ``SI`` quantities, ``SICompoundUnit``s don't do calculations but keep the connections to the ``SIUnit``s and the order of multiplication.

	``SICompoundUnit``s are usually constructed by multiplication / division of ``SIUnit``s, FIXME

	>>> h = search('h'); m = search('m')
	>>> print 1/h**2
	1/h^2
	>>> m/h
	<SICompoundUnit ((1, <SIUnit: 'metre' ('m')>, 1), (1, <SIUnit: 'hour' ('h')>, -1))>

	``SICompoundUnit``s can also be constructed from strings:

	>>> print SICompoundUnit("m/ms")
	m/ms
	"""

	@classmethod
	def decomposition_from_pure_string(cls, s):
		"""Convert a string containing only SI units (no numbers) to a list of (prefix, unit, power) tuples.

		Used for string to SI unit conversion.
		
		>>> SICompoundUnit.decomposition_from_pure_string("kgNkm/m")
		[(1, <SIUnit: 'kilogram' ('kg')>, 1), (1, <SIUnit: 'newton' ('N')>, 1), (1000, <SIUnit: 'metre' ('m')>, 1), (1, <SIUnit: 'metre' ('m')>, -1)]
		"""
		result = []
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
				inside = cls.decomposition_from_pure_string(s[1:end])
				if not pospow:
					inside = [(prefix, unit, -power) for (prefix, unit, power) in inside]
				for prefix, unit, power in inside:
					result.append((prefix, unit, power))

				s = s[end+1:]
				pospow = True
				continue

			for x in range(len(s),0,-1):
				try:
					thisunit = si.register.search_prefixed(s[:x])
				except LookupError:
                                    continue

				s = s[x:]
				if s.startswith("^"):
					power = int(s[1]) # FIXME if someone complains. will raise an exception if my assertion was wrong.
					s=s[2:]
				else:
					power = 1
				if not pospow:
					power = power * (-1)

				result.append((thisunit[0], thisunit[1], power))
				pospow = True
				break
			else:
				raise Exception("Can not convert to unit: %s"%s)
	
		return result

	def __new__(cls, argument):
		# allow construnction from string as well as from list
		if isinstance(argument, basestring):
			newself = tuple(cls.decomposition_from_pure_string(argument))
			return tuple.__new__(cls, newself)
		else:
			return tuple.__new__(cls, argument)

	def __repr__(self):
		return '<%s %s>'%(type(self).__name__, super(SICompoundUnit, self).__repr__())

	def __str__(self):
		# FIXME: be a little intelligent about what can be grouped together
		import si.prefixes

		ret = ""
		for (prefix, unit, power) in self:
			if power < 0:
				power = power * -1
				ret += "/"
			if prefix != 1:
				ret += si.prefixes.prefix_from_value(prefix)
			ret += unit.preferred_symbol(allow_unicode=True)
			if power != 1:
				ret += '^%s'%power

		if ret.startswith('/'):
			ret = '1'+ret

		return ret

	def to_unit(self):
		"""Multiply all components in the ``SICompoundUnit`` to an ``SI`` object

		>>> h = search('h'); m = search('m')
		>>> print 1/h**2
		1/h^2

		#>>> print (1/h).to_unit() # would fail with sympy
		#0.000277777777778 Hz

		#>>> print (1/h).to_unit() # would fail with builtin floats
		#1/3600 Hz
		"""
		result = 1
		for (prefix, unit, power) in self:
			result *= (prefix * unit.unit) ** power
                        # FIXME: does not do special handling for kg, resulting in gramm being called milli-kilogramm

		return result

        # BIG FIXME: SIUnits create SICompoundUnits by multiplication/division; these should be able to continue that process
