# encoding: utf8
"""
This module encapsulates useful classes and data for calculating with SI quantities.
Loosely based on the `English translation of the SI brochure`__.

.. __: http://www.bipm.org/utils/common/pdf/si_brochure_8_en.pdf

>>> from si.units.common import *
>>> print (1*bar)*(1*l)
100 J

Uses floats and python math by default. Override by setting SI.math to a math emulating module, SI.nonint to (a wrapper around) your numeric type, truediv to a good divsion function, and pow (see default function).

Caveats:

	* SI objects are purely mathematical (no physical concepts) and therefore can not have any notion of what they are *really* representing. Don't expect them to make a difference between Nm and J!
	* Python/IEEE floats are not ideal to represent negative powers of ten. Take the difference between mL and cm3 to know what I mean.
"""
from __future__ import division
import sys
import string
import warnings

import si.math

class MakesNoSense(Exception):
	"""Exception raised when impossible operations are attempted on SI objects, like adding seconds to candela."""

class Exponents(dict):
	"""Dictionary mapping symbolic bases to exponents."""
	def __str__(self):
		"""Standard string representation.
		
		>>> print Exponents({'m':1,'s':-2})
		m/s^2
		>>> print Exponents({'s':-1})
		/s
		>>> print Exponents({'a':1,'b':-2,'c':3,'d':-10})
		a c^3/(b^2 d^10)
		"""
		dpos=[x for x in self.items() if x[1]>0]
		dneg=[(x[0],-x[1]) for x in self.items() if x[1]<0]
		dpos.sort(lambda x,y:cmp(x[1],y[1]))
		dneg.sort(lambda x,y:cmp(x[1],y[1]))
		pospart,negpart=[],[]
		for part,d in [(pospart,dpos),(negpart,dneg)]:
			for s,n in d:
				part.append(unicode(s)+(n!=1 and "^%s"%n or ""))
		r=" ".join(pospart)
		if negpart:
			r+='/'
			if len(negpart)>1: r+='('
			r+=" ".join(negpart)
			if len(negpart)>1: r+=')'
		return r.strip()

class SI(tuple):
	"""SI quantity, storeed as a 2-tuple of value and a tuple storing the dimension (α to η)."""

	symbols=('m','kg','s','A','K','mol','cd') # for simple representation

	value=property(lambda self:self[0])
	dim=property(lambda self:self[1])
	unit=property(lambda self:SI((1,self.dim)))

	@staticmethod
	def _exponents_mul(A,B):
		return tuple([a+b for a,b in zip(A,B)])
	@staticmethod
	def _exponents_div(A,B):
		return tuple([a-b for a,b in zip(A,B)])

	def __add__(self,other):
		""">>> from si.units.common import *
		>>> print 1*m+2*m
		3 m"""
		if self.dim!=other.dim: raise MakesNoSense("Adding non-compatible quantities.")
		return SI((self.value+other.value,self.dim))
	def __sub__(self,other):
		""">>> from si.units.common import *
		>>> print (m+m)-m
		1 m"""
		if self.dim!=other.dim: raise MakesNoSense("Subtracting non-compatible quantities.")
		return SI((self.value-other.value,self.dim))
	def __mul__(self,other):
		""">>> from si.units.common import *
		>>> print 2*m
		2 m
		>>> print m*2
		2 m
		>>> print 2*m*m
		2 m^2
		>>> print 1/s * s
		1"""
		if not hasattr(other,'dim'):
			return SI((self.value*other,self.dim))
		newexp = self._exponents_mul(self.dim,other.dim)
		if not self._expsum(newexp):
			return self.value * other.value
		return SI((self.value*other.value,newexp))
	__rmul__=__mul__
	def __div__(self,other):
		""">>> from si.units.common import *
		>>> print (m*m)/m
		1 m
		>>> print (10*m)/2
		5 m
		>>> print (10*m)/(5*m)
		2"""
		if not hasattr(other,'dim'):
			return SI((si.math.truediv(self.value,other),self.dim))
		newexp = self._exponents_div(self.dim,other.dim)
		if not self._expsum(newexp):
			return si.math.truediv(self.value,other.value)
		return SI((si.math.truediv(self.value,other.value),newexp))
	__truediv__=__div__
	def __rdiv__(self,other):
		""">>> from si.units.common import *
		>>> print 5/Hz
		5 s"""
		if hasattr(other,'dim'):
			raise NotImplementedError("SI units can handle divisions themselves, no need to do this here")
		return SI((si.math.truediv(other,self.value),tuple(-x for x in self.dim)))
	__rtruediv__=__rdiv__
	def __pow__(self,exp):
		""">>> from si.units.common import *
		>>> print (5*m)**2
		25 m^2"""
		return SI((si.math.pow(self.value,exp),tuple(a*exp for a in self.dim)))

	def __cmp__(self,other):
		if self.dim!=other.dim: raise MakesNoSense("Comparing non-compatible quantities.")
		return cmp(self[0],other[0])
	def __nonzero__(self):
		return bool(self.value)

	def __lt__(self, other):
		return cmp(self, other)<0
	def __gt__(self, other):
		return cmp(self, other)>0
	def __le__(self, other):
		return cmp(self, other)<=0
	def __ge__(self, other):
		return cmp(self, other)>=0

	def using(self,unit):
		"""Get numeric value in given unit.
		Use this instead of division if you want to make sure that the units match. (Otherwise, an exception is raised.)

		How much is 1 m/s in attorparsec per microfortnight?

		>>> from si.units.exotic import *
		>>> print (1*m/s).using(apc/ufortnight) # doctest: +ELLIPSIS
		39.2004662878...
		"""
		if self.dim!=unit.dim: raise MakesNoSense("The quantity can not be expressed in that unit.")
		return self.value/unit.value

	def basestring(self):
		"""String representation using only powers of base units."""
		return "%s %s"%(self.value,Exponents(zip(self.symbols,self.dim)))
	def __repr__(self):
		return '<SI %s>'%self.basestring()

	@staticmethod
	def _expsum(u):
		return sum([abs(x) for x in u])

	def intelligentstring(self, unicode = True):
		"""Return a string representation using compound SI units. The function will roughly try to:

		- minimize the sum of absolute values of exponents:
		>>> from si.units.common import *
		>>> gravity=10*m/s/s; height=5*m; mass=5*kg
		>>> print gravity*height*mass
		250 J

		- avoid units with no positive exponents:
		>>> print 5/s
		5 Hz

		Will use unicode strings unless unicode is false.
		"""

		u_exact = []
		u_always = []

		for m in ModuleSIRegister.loadedmodules:
			for ru in m.units:
				if ru.map != "never": u_exact.append(ru)
				if ru.map == "always": u_always.append(ru)

		u_always.sort(cmp = lambda a,b: -cmp(self._expsum(a.unit.dim), self._expsum(b.unit.dim)))

		exactmatch = []
		for ru in u_exact:
			if ru.unit == self.unit:
				exactmatch.append(ru)

		if exactmatch:
			if len(exactmatch)>1:
				warnings.warn("More than one registered unit matches this quantity: %s."%exactmatch)
			decomposition = {exactmatch[0].preferred_symbol(unicode):1}
			remaining = self / exactmatch[0].unit
		else:
			decomposition = {}
			remaining = self
			last = None

			while hasattr(remaining, "dim") and (last is None or last != remaining):
				last = remaining
				currentexpsum=self._expsum(remaining.dim)
				for ru in u_always:
					div = remaining / ru.unit
					if not hasattr(div, "dim") or ( # we are through with this
								not sum([abs(a) < abs(b) for a,b in zip(remaining.dim, div.dim)]) # don't use factors that enlarge exponents
								and
								not sum([abs(a) < abs(b) for a,b in zip(remaining.dim, ru.unit.dim)]) # don't use factors larger than remaining
							) and self._expsum(div.dim)<currentexpsum: # "pays off"
						decomposition[ru.preferred_symbol(unicode)] = decomposition.get(ru.preferred_symbol(unicode),0) + 1
						remaining=div
						break

			# now for negative exponents

			last = None
			while hasattr(remaining, "dim") and (last is None or last != remaining): # copy/pasted from above, just changed operators. FIXME: enhance
				last = remaining
				currentexpsum=self._expsum(remaining.dim)
				for ru in u_always:
					div = remaining * ru.unit
					if not hasattr(div, "dim") or ( # we are through with this
								not sum([abs(a) < abs(b) for a,b in zip(remaining.dim, div.dim)]) # don't use factors that enlarge exponents
								and
								not sum([abs(a) < abs(b) for a,b in zip(remaining.dim, ru.unit.dim)]) # don't use factors larger than remaining
							) and self._expsum(div.dim)<currentexpsum: # "pays off"
						decomposition[ru.preferred_symbol(unicode)] = decomposition.get(ru.preferred_symbol(unicode),0) - 1
						remaining=div
						break

			assert not hasattr(remaining, "dim"), "Didn't catch all exponents. Base units are probably not registered!"

		if remaining == math.round(remaining):
			remaining = int(remaining)
		return "%s %s"%(remaining, Exponents(decomposition))
				
	def __unicode__(self): return self.intelligentstring(True)

	def __str__(self): return self.intelligentstring(False)


def _stringlist(o):
	if isinstance(o, basestring): return [o]
	if hasattr(o, "__len__"):
		return o
	else:
		return [o]

def _valid_python_name(s):
	return len([l for l in string.letters+"_" if s.startswith(l)]) and not len([l for l in s if l not in string.letters+string.digits+"_"])

class ModuleSIRegister(object):
	"""In a module, create a ``_register = ModuleSIRegister(locals())`` and add define units like ``_register.register(s**-1, "Hz", "herz", prefixes = list('YZEPTGMk'))``. Units will be made available for inclusion automatically, and prefixing is handled."""
	loadedmodules = []

	def __init__(self, locals):
		self.units = []

		self.locals = locals
		self.loadedmodules.append(self)
		self._prefix = False

	def register(self, unit, symbol, name, description = None, prefixes = None, map = "exact"):
		"""Add a unit.
		
		prefixes is a list of SI prefix names common for that unit (or True for all, or one of ``["kg","m2","m3"]`` for magic handling). map defines if and how the unit should be used to give names to SI quantities ("exact" to match only itself, "always" for normal use, "never")"""

		symbol = _stringlist(symbol)
		name = _stringlist(name)

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
	"""Container to store meta information about an ``SI``. Stores prefix preferences, name, symbol, description, and display preferences. Listed via ``ModuleSIRegister``s, which in turn have their own mechanism to be listed.
	
	Should in most cases be constructed via the ``ModuleSIRegister``s' ``resgister()`` function."""
	all_prefixes = list('YZEPTGMkhdcmunpfazy') + ["da"]
	def __init__(self, unit, symbol, name, description, prefixes, map):
		self.unit, self.symbol, self.name, self.description, self.prefixes, self.map = unit, symbol, name, description, prefixes, map

	def get_prefixed(self):
		"""Return a list of 2-tuples with prefixed python-usable name versions and the corresponding unit value."""
		import si.prefixes
		if not self.prefixes:
			return []
		elif self.prefixes == "kg":
			assert self.name == ["kilogram"], "Prefixing kg style only makes sense for kg. Fix me if I'm wrong."
			g = self.unit / 1000
			r = [("g", g)]
			for p in self.all_prefixes:
				if p != "k":
					r.append((p+"g", g * getattr(si.prefixes, p)))
			return r
		elif self.prefixes == "m2":
			assert self.name == ["square metre"], "Prefixing m2 style only makes sense for m2. Fix me if I'm wrong."
			r = []
			for p in self.all_prefixes:
				r.append((p+"m2", self.unit * getattr(si.prefixes, p)**2))
			return r
		elif self.prefixes == "m3":
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

	def get_python_names(self):
		"""Yield at least one name that can be used to address the unit in python. First (long) name will be used if all prefixes are unusable as python identifiers."""
		setone = False
		for n in self.symbol:
			if _valid_python_name(n):
				yield n
				setone = True
		if not setone:
			for n in self.name:
				if _valid_python_name(n):
					yield n
					break
			else:
				raise Exception("Can not register unit name.")

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
