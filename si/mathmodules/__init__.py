import sys
import si.math # the dummy module

def choose(module, localdict = None):
    """Load module (which can be, as of now, "python" or "sympy") as si.math, which will be used for all _further_ calculations.""" # pass localdict from the dummy module as the si.math module is not yet fully loaded and can not be accessed as si.math.__dict__
    #import imp
    #imp.load_module("si.math",*imp.find_module(module,__path__))    # worked without manualy tampering with si.math's locals, but didn't work from inside eggs

    if module=="python":
        import si.mathmodules.python as m
    elif module=="sympy":
        import si.mathmodules.sympy as m

    d = localdict or si.math.__dict__
    d.clear()
    d.update(m.__dict__)
    d['__name__'] = "si.math"
