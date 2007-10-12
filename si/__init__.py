# encoding: utf8
"""
This module encapsulates useful classes and data for calculating with SI quantities.
Loosely based on the English translation of the SI brochure
<http://www.bipm.org/utils/common/pdf/si_brochure_8_en.pdf>

>>> from si.units.common import *
>>> print (1*bar)*(1*l)
100.0 J

Uses floats and python math by default. Override by setting SI.math to a math emulating module, SI.nonint to (a wrapper around) your numeric type, truediv to a good divsion function, and pow (see default function).
"""
from __future__ import division
import sys
import string
import warnings

import math as math # override this 
def nonint(s):
	"""SI.nonint is used by prefixes and units to allow for flexible handling of non-integer numbers (integers are assumed to work in all situations).

	Passed s will roughly fit "($DECIMAL)(/$DECIMAL)?(+-$DECIMAL(/$DECIMAL))?", if you get the idea. +- indicates standard uncertainity, just in case some system cares, and can be discarded by most implementations."""
	if "+-" in s:
		assert len(s) == 2*s.index("+-")+2, "I think you got the standard uncertainities wrong. Fix me if it's me."
		s = s[:s.index("+-")]
	if "/" in s:
		s = s.split("/",1)
		return truediv(float(s[0]),float(s[1]))
	else:
		return float(s)
def truediv(a,b):
	"""Return a/b, both of which can be int, whatever is returned by nonint, or basically anything else."""
	if a/b == a//b:
		return a//b
	else:
		return a/b
pow = pow

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
		2 m^2"""
		if not hasattr(other,'dim'):
			return SI((self.value*other,self.dim))
		return SI((self.value*other.value,self._exponents_mul(self.dim,other.dim)))
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
			return SI((truediv(self.value,other),self.dim))
		if other.dim==self.dim: return truediv(self.value,other.value)
		return SI((truediv(self.value,other.value),self._exponents_div(self.dim,other.dim)))
	__truediv__=__div__
	def __rdiv__(self,other):
		""">>> from si.units.common import *
		>>> print 5/Hz
		5 s"""
		if hasattr(other,'dim'):
			raise NotImplementedError("SI units can handle divisions themselves, no need to do this here")
		return SI((truediv(other,self.value),tuple(-x for x in self.dim)))
	__rtruediv__=__rdiv__
	def __pow__(self,exp):
		""">>> from si.units.common import *
		>>> print (5*m)**2
		25 m^2"""
		return SI((pow(self.value,exp),tuple(a*exp for a in self.dim)))

	def __cmp__(self,other):
		if self.dim!=other.dim: raise MakesNoSense("Comparing non-compatible quantities.")
		return cmp(self[0],other[0])
	def __nonzero__(self):
		return bool(self.value)

	def using(self,unit):
		"""Get numeric value in given unit.

		>>> from si.units.exotic import *
		>>> (1*m/s).using(apc/ufortnight) # "how much is 1 m/s in attorparsec/microfortnight?"
		39.200466287804225
		"""
		if self.dim!=unit.dim: raise MakesNoSense("The quantity can not be expressed in that unit.")
		return self.value/unit.value

	def basestring(self):
		"""String representation using only powers of base units."""
		return "%s %s"%(self.value,Exponents(zip(self.symbols,self.dim)))
	def __repr__(self):
		return '<SI %s>'%self.basestring()

	def intelligentstring(self):
		"""Return a string representation using compound SI units. The function will try to

		- minimize the sum of absolute values of exponents: (this is only partially achieved)
		>>> from si.units.common import *
		>>> gravity=10*m/s/s; height=5*m; mass=5*kg
		>>> print gravity*height*mass
		250 J

		- avoid units with no positive exponents:
		>>> print 5/s
		5 Hz
		"""
		def expsum(u):
			return sum([abs(x) for x in u])

		u_exact = []
		u_always = []

		for m in ModuleSIRegister.loadedmodules:
			for ru in m.units:
				if ru.map != "never": u_exact.append(ru)
				if ru.map == "always": u_always.append(ru)

		exactmatch = []
		for ru in u_exact:
			if ru.unit == self.unit:
				exactmatch.append(ru)

		if exactmatch:
			if len(exactmatch)>1:
				warnings.warn("More than one registered unit matches this quantity.")
			unit = exactmatch[0].unit
			unit_symbol = exactmatch[0].preferred_symbol()
		else:
			u_always.sort(cmp = lambda a,b: -cmp(expsum(a.unit.dim), expsum(b.unit.dim)))

			decomposition={}

			lastunits=None
			remaining=self.dim
			while lastunits!=remaining:
				lastunits=remaining
				currentexpsum=expsum(remaining)
				for ru in u_always:
					div=self._exponents_div(remaining,ru.unit.dim)
					if expsum(div)+1<currentexpsum or (expsum(div)+1<=currentexpsum and max([x for x in remaining if x])<0 and not max([x for x in div if x]+[1])<0): # by dividing, another exponent is added (thus +1). substitution with equal number of exponents is only done to avoid negative exponents.
						decomposition[ru]=decomposition.get(ru,0)+1
						remaining=div
						break

			unit_symbol = dict((k.preferred_symbol(), v) for (k,v) in decomposition.iteritems())
			unit = 1
			for k,v in decomposition.iteritems():
				unit *= k.unit ** v

			for name,value in zip(self.symbols,remaining):
				assert name not in unit_symbol
				unit_symbol[name] = value
			unit *= SI((1, remaining))

			unit_symbol = Exponents(unit_symbol)
		
		return "%s %s"%(self / unit, unit_symbol)
				
	__unicode__=intelligentstring

	def __str__(self):
		return str(unicode(self))


def _stringlist(o):
	if isinstance(o, basestring): return [o]
	if hasattr(o, "__len__"):
		return o
	else:
		return [o]
def _valid_name(s):
	return len([l for l in string.letters+"_" if s.startswith(l)]) and not len([l for l in s if l not in string.letters+string.digits+"_"])
class ModuleSIRegister(object):
	"""In a module, create a _register = ModuleSIRegister(locals()) and add define units like _register.register(s**-1, "Hz", "herz", prefixes = list('YZEPTGMk')). Units will be made available for inclusion automatically, and prefixing is handled."""
	loadedmodules = []

	def __init__(self, locals):
		self.units = []

		self.locals = locals
		self.loadedmodules.append(self)
		self._prefix = False

	def register(self, unit, symbol, name, description = None, prefixes = None, map = "exact"):
		"""Add a unit.
		
		prefixes is a list of SI prefix names common for that unit (or True for all, or one of ["kg","m2","m3"] for magic handling). map defines if and how the unit should be used to give names to SI quantities ("exact" to match only itself, "always" for normal use, "never")"""

		symbol = _stringlist(symbol)
		name = _stringlist(name)

		ru = self.RegisteredSI(unit, symbol, name, description, prefixes, map)
		self.units.append(ru)

		for n in ru.get_names():
			self.locals[n] = unit
		if self._prefix:
			for n, pu in ru.get_prefixed():
				self.locals[n] = pu
	
	def prefix(self):
		self._prefix = True

		for ru in self.units:
			for n, pu in ru.get_prefixed():
				self.locals[n] = pu

	class RegisteredSI(object):
		all_prefixes = list('YZEPTGMkmunpfazy') + ["da"]
		def __init__(self, unit, symbol, name, description, prefixes, map):
			self.unit, self.symbol, self.name, self.description, self.prefixes, self.map = unit, symbol, name, description, prefixes, map

		def get_prefixed(self):
			import si.prefixes
			if not self.prefixes:
				return []
			if self.prefixes in ["m2","m3","kg"]:
				warnings.warn("Magic prefixes not yet implemented.")
				return []
			if self.prefixes == True:
				prefixes = self.all_prefixes
			else:
				prefixes = self.prefixes

			r = []
			for n in self.get_names():
				for p in prefixes:
					r.append((p+n, self.unit * getattr(si.prefixes, p)))
			return r
	
		def get_names(self):
			setone = False
			for n in self.symbol:
				if _valid_name(n):
					yield n
					setone = True
			if not setone:
				for n in self.name:
					if _valid_name(n):
						yield n
						break
				else:
					raise Exception("Can not register unit name.")

		def preferred_symbol(self):
			return self.symbol[0] if self.symbol else self.name[0]
	
		def __repr__(self):
			return "<RegisteredSI %r>"%self.symbol
