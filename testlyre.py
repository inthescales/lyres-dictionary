import unittest

from src.tests.form_tests import FormTests
from src.tests.gloss_tests import GlossTests
from src.tests.expression_tests import ExpressionTests
from src.tests.diachronizer_tests import DiachronizerTests

suite = unittest.TestSuite()
loader = unittest.defaultTestLoader

# Add test cases
suite.addTest(loader.loadTestsFromTestCase(FormTests))
suite.addTest(loader.loadTestsFromTestCase(GlossTests))
suite.addTest(loader.loadTestsFromTestCase(ExpressionTests))
suite.addTest(loader.loadTestsFromTestCase(DiachronizerTests))

# Run tests
runner = unittest.TextTestRunner()
runner.run(suite) 
