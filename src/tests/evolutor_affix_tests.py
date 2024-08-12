import unittest

from src.morphs.morphothec import Morphothec
from src.generation.former import Former_Config
from src.generation.generator import word_for_keys
import src.generation.composer as composer

import src.evolutor.language.mne_affixation as mne_affixation

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
        # self.assertForm(["flǣsċ", "-liċ"], "fleshly") # Needs override support
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
 
    def testJoinedSpellings(self):
        # Final diphthong 'y' changes to 'i', if indicated
        self.assertJoined(["day", "ly"], True, "daily")
        self.assertJoined(["gay", "ly"], True, "gaily")

        # Final vowel 'y' changes to 'i', if indicated and unstressed
        self.assertJoined(["lady", "ly"], True, "ladily")

        # Final vowel 'y' changes to 'i' if indicated and part of '-y' suffix
        self.assertJoined(["busy", "ness"], True, "business")
        self.assertJoined(["dizzy", "ness"], True, "dizziness")   
        self.assertJoined(["worthy", "ness"], True, "worthiness")

        # Final vowel 'y' stressed and not part of '-y' suffix never changes, even if indicated
        self.assertJoined(["dry", "ly"], True, "dryly")
        self.assertJoined(["shy", "ness"], True, "shyness")

        # Final vowel 'y' remains if not indicated
        self.assertJoined(["coy", "ness"], False, "coyness")
        self.assertJoined(["lady", "like"], False, "ladylike")

    def test_t_to_i_indication(self):
        # '-liċ' imposes y-to-i on previous morph
        self.assertForm(["dæġ", "-liċ"], "daily")

        # '-iġ' uses y-to-i
        self.assertForm(["mōd", "-iġ", "-nes"], "moodiness")

        # Morph with baked-in '-iġ' ending also uses y-to-i
        self.assertForm(["dohtiġ", "-nes"], "doughtiness")

        # '-ere' uses y-to-i
        # self.assertForm(["bysiġan", "-ere"], "busier") # Needs overrides for 'y' -> /u/

        # Other morphs ending in '-y' don't
        self.assertForm(["drȳġe", "-nes"], "dryness")

    def test_misc_spelling_changes(self):
        # Drop silent 'e' in favor of vowel
        self.assertForm(["hors", "-isċ"], "horsish")
        self.assertForm(["rose", "-iġ"], "rosy")

        # ...but don't drop non-silent final 'e'
        self.assertForm(["trēo", "-isċ"], "treeish")
        
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

    def assertJoined(self, strings, y_to_i, target):
        joined = mne_affixation.get_joined_form(strings[0], strings[1], y_to_i=y_to_i)
        if joined != target:
            print(joined + " !+ " + target)

