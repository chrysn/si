import sys
import unittest, doctest

def all():
    suite = unittest.TestSuite()
    import si, si.register, si.pylab
    suite.addTests(doctest.DocTestSuite(si))
    suite.addTests(doctest.DocTestSuite(si.register))
    suite.addTests(doctest.DocTestSuite(si.units))
    suite.addTests(doctest.DocTestSuite(si.pylab))

    import si.mathmodules.sympy
    suite.addTests(doctest.DocTestSuite(si.mathmodules.sympy)) # will test everything itself. add new tests there as well!

    # to test if everything works, uncomment the block containing "degree" in unit_from_string
    
    return suite
