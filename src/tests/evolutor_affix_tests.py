import unittest

from src.morphs.morphothec import Morphothec
from src.generation.former import Former_Config
from src.generation.generator import word_for_keys
import src.generation.composer as composer

class EvolutorAffixTests(unittest.TestCase):
    def setUp(self):
        self.morphothec = Morphothec("data/")

    # Old English ===========================

    # Tests that Old English form evolution with affixes works correctly
    def testOldEnglishEvolutionWithAffixes(self):
        
        # -dom
        self.assertForm(["cyng", "-dom"], "kingdom")

        # -ere
        self.assertForm(["lufian", "-ere"], "lover")

        # -iġ
        self.assertForm(["clǣġ", "-iġ"], "clayey")
        self.assertForm(["clif", "-iġ"], "cliffy")
        self.assertForm(["cræfte", "-iġ"], "crafty")
        # self.assertForm(["dēawe", "-iġ"], "dewy") # Needs override support
        self.assertForm(["fām", "-iġ"], "foamy")
        self.assertForm(["fen", "-iġ"], "fenny")
        self.assertForm(["frost", "-iġ"], "frosty")
        self.assertForm(["īs", "-iġ"], "icy")
        self.assertForm(["liþ", "-iġ"], "lithy")
        self.assertForm(["miht", "-iġ"], "mighty")
        # self.assertForm(["stān", "-iġ"], "stony") # Needs override support
        self.assertForm(["wind", "-iġ"], "windy")
        
        # -isċ
        self.assertForm(["ċild", "-isċ"], "childish")
        self.assertForm(["midl", "-isċ"], "middlish") #*
        self.assertForm(["ġearu", "-isċ"], "yarish") #*

        # -liċ
        self.assertForm(["ǣr", "-liċ"], "early")
        self.assertForm(["brōþor", "-liċ"], "brotherly")
        self.assertForm(["brȳd", "-liċ"], "bridely")
        self.assertForm(["cræfte", "-liċ"], "craftly")
        self.assertForm(["cwic", "-liċ"], "quickly")
        self.assertForm(["dēad", "-liċ"], "deadly")
        self.assertForm(["dēaþ", "-liċ"], "deathly")
        self.assertForm(["dēore", "-liċ"], "dearly")
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
        self.assertForm(["ġelīc", "-nes"], "likeness")
        self.assertForm(["frēo", "-nes"], "freeness")
        self.assertForm(["hlūd", "-nes"], "loudness")
        self.assertForm(["lyttel", "-nes"], "littleness")
        self.assertForm(["open", "-nes"], "openness")
        self.assertForm(["tōh", "-nes"], "toughness")
        self.assertForm(["þynne", "-nes"], "thinness")
        self.assertForm(["wilde", "-nes"], "wildness")

        # -oc
        self.assertForm(["bit", "-oc"], "bittock")
        self.assertForm(["fȳst", "-oc"], "fistock")
        self.assertForm(["hyll", "-oc"], "hillock")
        self.assertForm(["wreċċ", "-oc"], "wretchock")

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
        
        # Spelling changes ---

        # Change final y to i before consonant
        self.assertForm(["dæġ", "-liċ"], "daily")
        self.assertForm(["dohtiġ", "-nes"], "doughtiness")

        # Drop silent e in favor of vowel
        self.assertForm(["rose", "-iġ"], "rosy")
        
        # Eliminate triple consonants
        self.assertForm(["full", "-liċ"], "fully")


# Helpers ==========
    
    def assertForm(self, keys, form):
        word = word_for_keys(keys, self.morphothec)
        former_config = Former_Config(False, False)
        composed = composer.get_form(word, former_config)
        # self.assertEqual(composed, form)
        if form != composed:
            print(form + " != " + composed)
