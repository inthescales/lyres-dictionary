import unittest

from src.morphothec import Morphothec
from src.generator import word_for_keys
import src.composer as composer

class EvolutionAffixTests(unittest.TestCase):
    def setUp(self):
        self.morphothec = Morphothec("data/")

    # Old English ===========================

    # Tests that Old English form evolution with affixes works correctly
    def testOldEnglishEvolutionWithAffixes(self):
        
        # -iġ
        self.assertForm(["wind", "-iġ"], "windy")
        
        # -liċ
        # self.assertForm(["brōþor", "-liċ"], "brotherly") # Need rule for regular shortening of ō in middle english before -ðer / -der
        self.assertForm(["brȳd", "-liċ"], "bridely")
        self.assertForm(["frēond", "-liċ"], "friendly")
        self.assertForm(["heofon", "-liċ"], "heavenly")

        # -nes
        self.assertForm(["frēond", "-liċ", "-nes"], "friendliness")

        

# Helpers ==========
    
    def assertForm(self, keys, form):
        word = word_for_keys(keys, self.morphothec)
        composed = composer.get_form(word)
        self.assertEqual(composed, form)
