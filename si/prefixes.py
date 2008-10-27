# encoding: utf8

from si.math import pow
Y = yotta = 10**24
Z = zetta = 10**21
E = exa = 10**18
P = peta = 10**15
T = tera = 10**12
G = giga = 10**9
M = mega = 10**6
k = kilo = 10**3
h = hecto = 10**2
da = deca = 10**1
d = deci = pow(10,-1)
c = centi = pow(10,-2)
m = milli = pow(10,-3)
u = micro = pow(10,-6) # would have to be μ or µ. FIXME: hardcoded in register.search_prefixed
n = nano = pow(10,-9)
p = pico = pow(10,-12)
f = femto = pow(10,-15)
a = atto = pow(10,-18)
z = zepto = pow(10,-21)
y = yocto = pow(10,-24)

del pow

def prefix_from_value(value, short=True): # FIXME: this could use a more sophisticated system as present for SI Units (or would this mean overkill?)
    """Convert a numerical value to an SI prefix (by default using the short form)"""

    import si.prefixes

    def mycmp(a, b): # FIXME: decorate/sort/undecorate is probably faster
        return cmp(len(a), len(b))
    variants = sorted((k for (k,v) in vars(si.prefixes).iteritems() if v==value), cmp=mycmp)
    if short:
        return variants[0]
    else:
        return variants[-1]
