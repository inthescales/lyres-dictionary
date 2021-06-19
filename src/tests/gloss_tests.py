import unittest

from src.morphothec import Morphothec
from src.generator import word_for_keys
import src.composer as composer

class GlossTests(unittest.TestCase):
    def setUp(self):
        self.morphothec = Morphothec(["src/tests/gloss_test_morphs.json"])

    def testSuffixation(self):
        # Single suffixes
        self.assertGloss(["avis", "al"], "pertaining to birds")
        self.assertGloss(["avis", "ity"], "the quality of being a bird")
        
        self.assertGloss(["gravis", "ity"], "the quality of being heavy")
        self.assertGloss(["gravis", "esce"], "to become heavy")
        
        self.assertGloss(["iacere", "nt"], "throwing")
        self.assertGloss(["iacere", "ble"], "able to be thrown")
        
        # Multiple suffixes
        self.assertGloss(["iacere", "nt", "al"], "pertaining to throwing")
        self.assertGloss(["iacere", "ble", "ity"], "the quality of being able to be thrown")
        self.assertGloss(["iacere", "nt", "al", "ity"], "the quality of being pertaining to throwing")
        
        # Separate link and final glosses
        self.assertGloss(["iacere", "ion"], "the act of throwing")
        self.assertGloss(["iacere", "ion", "al"], "pertaining to throwing")
        
        
    # Helpers ===============================
    
    def assertGloss(self, keys, gloss):
        word = word_for_keys(keys, self.morphothec)
        composed = composer.get_definition(word)
        self.assertEqual(composed, gloss)

if __name__ == '__main__':    
    unittest.main()