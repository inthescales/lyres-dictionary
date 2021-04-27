import unittest

from src.tests.form_tests import FormTests

suite = unittest.TestSuite()
loader = unittest.defaultTestLoader

# Add test cases
suite.addTest(loader.loadTestsFromTestCase(FormTests))

# Run tests
runner = unittest.TextTestRunner()
runner.run(suite) 
