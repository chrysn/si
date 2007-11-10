"""Module for (annotated) unit housekeeping; see ``ModuleSIRegister``."""
from __future__ import division
import string

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
		"""A wrapper around SIAnnotation to add a unit with symbols and names (can be string/unicode or list thereof).
		
		prefixes is a list of SI prefix names common for that unit (or True for all, or one of ``["kg","m2","m3"]`` for magic handling). map defines if and how the unit should be used to give names to SI quantities ("always" for normal use, "exact" to match only scalar multiples of the unit, "never") """

		symbol = self._stringlist(symbol)
		name = self._stringlist(name)

		ru = SIAnnotation(unit, symbol, name, description, prefixes, map)
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

class SIAnnotation(object):
	"""Container to store meta information about an ``SI`` unit. Stores prefix preferences, name, symbol, description, and display preferences. Listed via ``ModuleSIRegister``s, which in turn have their own mechanism to be listed.
	
	Should in most cases be constructed via the ``ModuleSIRegister``s' ``register()`` function."""

	all_prefixes = list('YZEPTGMkhdcmunpfazy') + ["da"]
	def __init__(self, unit, symbol, name, description, prefixes, map):
		"""See ``ModuleSIRegister.register`` for details."""
		self.unit, self.symbol, self.name, self.description, self.prefixes, self.map = unit, symbol, name, description, prefixes, map

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
			return self.symbol[0] if self.symbol else self.name[0]
		else:
			for s in self.symbol + self.name:
				if not isinstance(s, unicode):
					return s
			raise Exception, "No non-unicode symbol available."

	def __repr__(self):
		return "<SIAnnotation %r>"%self.symbol
