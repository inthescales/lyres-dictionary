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
        self.assertGloss(["vehere", "nt"], "carrying")
        self.assertGloss(["vehere", "ion"], "the act of carrying")
        
        # Multiple suffixes
        self.assertGloss(["iacere", "nt", "al"], "pertaining to throwing")
        self.assertGloss(["iacere", "ble", "ity"], "the quality of being able to be thrown")
        self.assertGloss(["iacere", "nt", "al", "ity"], "the quality of being pertaining to throwing")
        
        # Separate link and final glosses
        self.assertGloss(["iacere", "ion"], "the act of throwing")
        self.assertGloss(["iacere", "ion", "al"], "pertaining to throwing")
    
    def testPrefixation(self):
        # Prepositional verb prefixes
        self.assertGloss(["ad", "iacere"], "to throw to")
        self.assertGloss(["in", "iacere"], "to throw in")
        self.assertGloss(["ad", "vehere"], "to carry to")
        self.assertGloss(["in", "vehere"], "to carry in")
        
        # Non-prepositional prefixes
        self.assertGloss(["re-again", "iacere"], "to throw again")
        self.assertGloss(["re-again", "vehere"], "to carry again")
        
        # Both kinds of prefixes
        self.assertGloss(["re-again", "in", "iacere"], "to throw in again")
        self.assertGloss(["re-again", "ad", "vehere"], "to carry to again")
    
    def testCombinedAffixation(self):
        # Test suffixes and prefixes together
        self.assertGloss(["ad", "iacere", "nt"], "throwing to")
        self.assertGloss(["in", "vehere", "ble"], "able to be carried in")
        self.assertGloss(["re-again", "ad", "iacere", "nt"], "throwing to again")
        self.assertGloss(["re-again", "in", "vehere", "ble"], "able to be carried in again") 
        
    # Helpers ===============================
    
    def assertGloss(self, keys, gloss):
        word = word_for_keys(keys, self.morphothec)
        composed = composer.get_definition(word)
        self.assertEqual(composed, gloss)

if __name__ == '__main__':    
    unittest.main()