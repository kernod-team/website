import unittest
tests = unittest.defaultTestLoader.discover('tests')
unittest.TextTestRunner(verbosity=2).run(tests)
