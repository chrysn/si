def choose(module):
    """Load module (which can be, as of now, "python" or "sympy") as si.math, which will be used for all _further_ calculations."""
    import imp
    imp.load_module("si.math",*imp.find_module(module,__path__))
