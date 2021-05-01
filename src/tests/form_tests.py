import unittest

from src.morphothec import Morphothec
from src.generator import word_for_keys
import src.composer as composer

class FormTests(unittest.TestCase):
    def setUp(self):
        self.morphothec = Morphothec(["data/morphs-latin.json", "data/morphs-greek.json"])

    # Tests that prefix sound assimilation resolves correctly.
    def testPrefixAssimilation(self):
        # ad
        self.assertForm(["ad", "ducere", "ion"], "adduction")
        self.assertForm(["ad", "educare", "ion"], "adeducation") #*
        self.assertForm(["ad", "jurare"], "adjure")
        self.assertForm(["ad", "mirari", "ion"], "admiration")
        self.assertForm(["ad", "optare", "ion"], "adoption")
        self.assertForm(["ad", "venire", "ure"], "adventure")
        
        # ad -> a
        # As in 'adapt'
        
        # ad doubling
        self.assertForm(["ad", "cedere", "ion"], "accession")
        self.assertForm(["ad", "figere", "ion"], "affixation")
        self.assertForm(["ad", "gradi", "ive"], "aggressive")
        self.assertForm(["ad", "ludere", "ion"], "allusion")
        self.assertForm(["ad", "nuntiare", "ion"], "annunciation")
        self.assertForm(["ad", "parere", "nt"], "apparent")
        self.assertForm(["ad", "rogare", "nt"], "arrogant")
        self.assertForm(["ad", "serere", "ion"], "assertion")
        self.assertForm(["ad", "serere", "ion"], "assertion")
        
        # ad -> ac
        self.assertForm(["ad", "quaerere", "ion"], "acquisition")
        
        # ad -> ab
        # As in 'abbreviate'
        

    # Miscellaneous tests confirming that real words have the correct forms.
    def testActualForms(self):        
        self.assertForm(["com", "venire", "ion"], "convention")
    
    # Helpers ==========
    
    def assertForm(self, keys, form):
        word = word_for_keys(keys, self.morphothec)
        self.assertEqual(composer.get_form(word), form)

if __name__ == '__main__':    
    unittest.main()