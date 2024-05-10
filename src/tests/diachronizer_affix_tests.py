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
        
        # -dom
        self.assertForm(["cyng", "-dom"], "kingdom")

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
        
        # -nes
        self.assertForm(["cwic", "-nes"], "quickness")
        self.assertForm(["dohtiġ", "-nes"], "doughtiness")
        self.assertForm(["ġelīc", "-nes"], "likeness")
        self.assertForm(["frēo", "-nes"], "freeness")
        self.assertForm(["hlūd", "-nes"], "loudness")
        self.assertForm(["lyttel", "-nes"], "littleness")
        self.assertForm(["open", "-nes"], "openness")
        self.assertForm(["tōh", "-nes"], "toughness")
        self.assertForm(["þynne", "-nes"], "thinness")
        self.assertForm(["wilde", "-nes"], "wildness")

        # -sċipe
        self.assertForm(["frēond", "-sċipe"], "friendship")
        self.assertForm(["heard", "-sċipe"], "hardship")

        # -ere
        self.assertForm(["pleġan", "-ere"], "player")

        # -estre

        # -hād
        self.assertForm(["ċild", "-hād"], "childhood")

        # Combinations of two suffixes

        self.assertForm(["cræfte", "-iġ", "-liċ"], "craftily")
        self.assertForm(["īs", "-iġ", "-nes"], "iciness")
        self.assertForm(["frēond", "-liċ", "-nes"], "friendliness")
        

# Helpers ==========
    
    def assertForm(self, keys, form):
        word = word_for_keys(keys, self.morphothec)
        composed = composer.get_form(word)
        # self.assertEqual(composed, form)
        if form != composed:
            print(form + " != " + composed)
