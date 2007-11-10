import sys
import unittest, doctest

def all():
    suite = unittest.TestSuite()
    import si
    suite.addTests(doctest.DocTestSuite(si))
    first_si = si

    import si.mathmodules.sympy
    suite.addTests(doctest.DocTestSuite(si.mathmodules.sympy))

    suite.addTests(doctest.DocTestSuite(si))
    
    return suite
