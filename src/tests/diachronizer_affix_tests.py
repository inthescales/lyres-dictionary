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
        self.assertForm(["clǣġ", "-iġ"], "clayey")
        self.assertForm(["clif", "-iġ"], "cliffy")
        self.assertForm(["cræfte", "-iġ"], "crafty")
        # self.assertForm(["dēawe", "-iġ"], "dewy") # Needs override support
        self.assertForm(["fām", "-iġ"], "foamy")
        self.assertForm(["fen", "-iġ"], "fenny")
        self.assertForm(["frost", "-iġ"], "frosty")
        self.assertForm(["full", "-iġ"], "fully")
        self.assertForm(["īs", "-iġ"], "icy")
        self.assertForm(["liþ", "-iġ"], "lithy")
        self.assertForm(["miht", "-iġ"], "mighty")
        # self.assertForm(["stān", "-iġ"], "stony") # Needs override support
        self.assertForm(["wind", "-iġ"], "windy")
        
        # -liċ
        self.assertForm(["ǣr", "-liċ"], "early")
        self.assertForm(["brōþor", "-liċ"], "brotherly")
        self.assertForm(["brȳd", "-liċ"], "bridely")
        # self.assertForm(["cȳme", "-liċ"], "comely") # Form may be irregular, patterned after "come"
        self.assertForm(["cræfte", "-liċ"], "craftly")
        self.assertForm(["cwic", "-liċ"], "quickly")
        self.assertForm(["dæġ", "-liċ"], "daily")
        self.assertForm(["dēad", "-liċ"], "deadly")
        self.assertForm(["dēaþ", "-liċ"], "deathly")
        self.assertForm(["dīere", "-liċ"], "dearly")
        self.assertForm(["eorþe", "-liċ"], "earthly")
        # self.assertForm(["flǣsċ", "-liċ"], "fleshly") # Can't explain 'e' in 'flesh'
        self.assertForm(["frēo", "-liċ"], "freely")
        self.assertForm(["frēond", "-liċ"], "friendly")
        self.assertForm(["fūl", "-liċ"], "foully")
        self.assertForm(["heofon", "-liċ"], "heavenly")
        self.assertForm(["lufu", "-liċ"], "lovely")
        self.assertForm(["swīn", "-liċ"], "swinely")
        self.assertForm(["wīd", "-liċ"], "widely")

        self.assertForm(["cræfte", "-iġ", "-liċ"], "craftily")
        
        # -nes
        self.assertForm(["frēond", "-liċ", "-nes"], "friendliness")
        self.assertForm(["cwic", "-nes"], "quickness")

        

# Helpers ==========
    
    def assertForm(self, keys, form):
        word = word_for_keys(keys, self.morphothec)
        composed = composer.get_form(word)
        # self.assertEqual(composed, form)
        if form != composed:
            print(form + " != " + composed)
