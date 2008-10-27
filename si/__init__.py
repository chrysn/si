# encoding: utf8
"""
This module encapsulates useful classes and data for calculating with SI quantities.
Loosely based on the `English translation of the SI brochure`__.

.. __: http://www.bipm.org/utils/common/pdf/si_brochure_8_en.pdf

>>> from si.common import *
>>> print (1*bar)*(1*l)
100 J

You can also extract additional information about units:

>>> from si.register import search
>>> search("m").description
'SI base unit of length'

Uses floats and python math by default. Override by setting SI.math to a math emulating module, SI.nonint to (a wrapper around) your numeric type, truediv to a good divsion function, and pow (see default function).

Caveats:

	* SI objects are purely mathematical (no physical concepts) and therefore can not have any notion of what they are *really* representing. Don't expect them to make a difference between Nm and J!
	* Python/IEEE floats are not ideal to represent negative powers of ten. Take the difference between mL and cm3 to know what I mean.
	* When using SI units in connection with other objects emulating mathematical behavior, you will have to take care of the sequence when multiplying, although SI objects themselves are commutative. For example, until `a bug in sympy`__ is fixed, you have to write ``kg*sympify("1/10")`` instead of ``sympify("1/10")*kg``.

.. __: http://code.google.com/p/sympy/issues/detail?id=432
"""
from __future__ import division
import sys
import warnings

import si.register
import si.math

class MakesNoSense(Exception):
	"""Exception raised when impossible operations are attempted on SI objects.
	
	>>> from si.common import *
	>>> m + s
	Traceback (most recent call last):
	  ...
	MakesNoSense: Adding non-compatible quantities.
	"""

class Exponents(dict):
	"""Dictionary mapping symbolic bases to exponents."""
	def _posneg(self):
		pos=[x for x in self.items() if x[1]>0]
		neg=[(x[0],-x[1]) for x in self.items() if x[1]<0]
		pos.sort(lambda x,y:cmp(x[1],y[1]))
		neg.sort(lambda x,y:cmp(x[1],y[1]))
		return pos, neg
	def __str__(self):
		"""Standard string representation.
		
		>>> print Exponents({'m':1,'s':-2})
		m/s^2
		>>> print Exponents({'s':-1})
		/s
		>>> print Exponents({'a':1,'b':-2,'c':3,'d':-10})
		a c^3/(b^2 d^10)
		"""
		pos, neg = self._posneg()
		pospart,negpart=[],[]
		for part,d in [(pospart,pos),(negpart,neg)]:
			for s,n in d:
				part.append(unicode(s)+(n!=1 and "^%s"%n or ""))
		r=" ".join(pospart)
		if negpart:
			r+='/'
			if len(negpart)>1: r+='('
			r+=" ".join(negpart)
			if len(negpart)>1: r+=')'
		return r.strip()

	def tex(self, use_over = False):
		"""TeX math mode representation.
		
		>>> print Exponents({'m':1,'s':-2}).tex()
		m/s^2
		>>> print Exponents({'s':-1}).tex(use_over = True)
		{1 \\over s}
		"""
		pos, neg = self._posneg()
		pospart,negpart=[],[]
		for part,d in [(pospart,pos),(negpart,neg)]:
			for s,n in d:
				if n==1:
					part.append(s)
				else:
					n = str(n)
					if len(n)>1: n="{%s}"%n
					part.append(unicode(s)+"^"+n)
		if use_over and negpart:
			pospart = pospart or ["1"]
			return r"{%s \over %s}"%(" ".join(pospart)," ".join(negpart))
		else:
			r = " ".join(pospart)
			if negpart:
				r += "/"
				if len(negpart)>1: r+= r"\left("
				r += " ".join(negpart)
				if len(negpart)>1: r+= r"\right)"
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
		if not hasattr(other, "dim") or self.dim!=other.dim:
			raise MakesNoSense("Comparing non-compatible quantities.")
		return cmp(self[0],other[0])
	def __nonzero__(self):
		return bool(self.value)

	def __lt__(self, other):
		""">>> from si.units.common import *
		>>> 1*m < 5*s
		Traceback (most recent call last):
		  ...
		MakesNoSense: Comparing non-compatible quantities.
		"""
		return self.__cmp__(other)<0
	def __gt__(self, other):
		""">>> from si.units.common import *
		>>> 1*m > 1
		Traceback (most recent call last):
		  ...
		MakesNoSense: Comparing non-compatible quantities.
		"""
		return self.__cmp__(other)>0
	def __le__(self, other):
		return self.__cmp__(other)<=0
	def __ge__(self, other):
		return self.__cmp__(other)>=0

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

	def _decomposition(self):
		u_exact = []
		u_always = []

		for m in si.register.ModuleSIRegister.loadedmodules:
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
			decomposition = {exactmatch[0]:1}
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
						decomposition[ru] = decomposition.get(ru,0) + 1
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
						decomposition[ru] = decomposition.get(ru,0) - 1
						remaining=div
						break

			assert not hasattr(remaining, "dim"), "Didn't catch all exponents. Base units are probably not registered!"

		remaining = math.simplest_form(remaining)
		return (remaining, decomposition)

	def intelligentstring(self, unicode = True):
		"""Return a string representation using compound SI units of already loaded modules. The function will roughly try to:

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
		remaining, decomposition = self._decomposition()

		return "%s %s"%(remaining, Exponents([(unit.preferred_symbol(unicode), power) for (unit, power) in decomposition.iteritems()]))

	def tex(self, use_over = False):
		"""Return a TeX math mode representation, using the same logic as ``intelligentstring``.

		>>> from si.common import *
		>>> print (5*m/s).tex(use_over=True)
		5 {m \\over s}
		"""
		remaining, decomposition = self._decomposition()

		if hasattr(remaining, "tex"):
			remaining = remaining.tex() # if it looks like a ghost from the future and talks like a ghost from the future, assume it is a ghost from the future. (pro-active ducktyping)

		return "%s %s"%(remaining, Exponents([(unit.tex(), power) for (unit, power) in decomposition.iteritems()]).tex(use_over = use_over))
				
	def __unicode__(self): return self.intelligentstring(True)

	def __str__(self): return self.intelligentstring(False)

