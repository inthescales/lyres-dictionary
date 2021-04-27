import unittest

from src.morphothec import Morphothec
from src.generator import word_for_keys
import src.composer as composer

class FormTests(unittest.TestCase):
    def setUp(self):
        self.morphothec = Morphothec(["data/morphs-latin.json", "data/morphs-greek.json"])

    def testActualForms(self):
        def testForm(keys, form):
            word = word_for_keys(keys, self.morphothec)
            self.assertEqual(composer.get_form(word), form)
        
        testForm(["com", "venire", "ion"], "convention")
        
if __name__ == '__main__':    
    unittest.main()