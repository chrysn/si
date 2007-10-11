import doctest

def all():
    import si
    return doctest.DocTestSuite(si)
