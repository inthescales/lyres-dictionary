import unittest

from src.tests.form_tests import FormTests
from src.tests.gloss_tests import GlossTests

suite = unittest.TestSuite()
loader = unittest.defaultTestLoader

# Add test cases
suite.addTest(loader.loadTestsFromTestCase(FormTests))
suite.addTest(loader.loadTestsFromTestCase(GlossTests))

# Run tests
runner = unittest.TextTestRunner()
runner.run(suite) 
