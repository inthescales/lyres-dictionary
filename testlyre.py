import unittest

from src.tests.form_tests import FormTests
from src.tests.gloss_tests import GlossTests
from src.tests.expression_tests import ExpressionTests

suite = unittest.TestSuite()
loader = unittest.defaultTestLoader

# Add test cases
suite.addTest(loader.loadTestsFromTestCase(FormTests))
suite.addTest(loader.loadTestsFromTestCase(GlossTests))
suite.addTest(loader.loadTestsFromTestCase(ExpressionTests))

# Run tests
runner = unittest.TextTestRunner()
runner.run(suite) 
