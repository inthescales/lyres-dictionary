import unittest

from src.tests.form_tests import FormTests
from src.tests.gloss_tests import GlossTests
from src.tests.expression_tests import ExpressionTests
from src.tests.evolutor_tests import EvolutorTests
from src.tests.evolutor_affix_tests import EvolutorAffixTests
from src.tests.helper_tests import HelperTests
from src.tests.past_participle_tests import PastParticipleTests
from src.tests.metadata_tests import MetadataTests

suite = unittest.TestSuite()
loader = unittest.defaultTestLoader

# Add test cases
suite.addTest(loader.loadTestsFromTestCase(FormTests))
suite.addTest(loader.loadTestsFromTestCase(GlossTests))
suite.addTest(loader.loadTestsFromTestCase(ExpressionTests))
suite.addTest(loader.loadTestsFromTestCase(EvolutorTests))
suite.addTest(loader.loadTestsFromTestCase(EvolutorAffixTests))
suite.addTest(loader.loadTestsFromTestCase(PastParticipleTests))
suite.addTest(loader.loadTestsFromTestCase(HelperTests))
suite.addTest(loader.loadTestsFromTestCase(MetadataTests))

# Run tests
runner = unittest.TextTestRunner()
runner.run(suite) 
