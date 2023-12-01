import unittest

import diachronizer as diachronizer

class DiachronizerTests(unittest.TestCase):
    # def setUp(self):

    def testFormFromOE(self):
        # A
        self.assertForm("mann", "man")
        self.assertForm("lamb", "lamb")
        self.assertForm("sang", "sang")
        self.assertForm("sacc", "sack")
        self.assertForm("assa", "ass")
        self.assertForm("fæþm", "fathom")
        self.assertForm("sæt", "sat")
        self.assertForm("æt", "at")
        self.assertForm("mæsse", "mass")
        self.assertForm("weax", "wax")
        self.assertForm("healf", "half")
        self.assertForm("āsci|an", "ask")
        self.assertForm("fǣtt", "fat")
        self.assertForm("læst|an", "last")
        # self.assertForm("blēddre", "bladder")
        self.assertForm("blǣddre", "bladder")
        # self.assertForm("brēmbel", "bramble")
        self.assertForm("brǣmbel", "bramble")
        self.assertForm("swan", "swan")
        self.assertForm("wasċ|an", "wash")
        self.assertForm("wann", "wan")
        self.assertForm("swæþ", "swath")
        self.assertForm("wæsp", "wasp")
        self.assertForm("wealwi|an", "wallow")
        self.assertForm("swealwe", "swallow")
        self.assertForm("heard", "hard")
        self.assertForm("ærc", "ark")
        self.assertForm("swearm", "swarm")
        self.assertForm("sweart", "swart")
        self.assertForm("weardi|an", "ward")
        self.assertForm("wearm", "warm")
        self.assertForm("wearni|an", "warn")
        self.assertForm("smæl", "small")
        self.assertForm("all", "all")
        self.assertForm("walci|an", "walk")
        # self.assertForm("ælmesse", "alms")
        self.assertForm("palm", "palm")
        self.assertForm("glæs", "glass")
        self.assertForm("græs", "grass")
        self.assertForm("pæþ", "path")
        self.assertForm("æfter", "after")
        self.assertForm("nama", "name")
        
        self.assertForm("nacod", "naked")
        self.assertForm("bac|an", "bake")
        # self.assertForm("æcer", "acre") # Irregular development due to early borrowing into latin and french
        # self.assertForm("hwæl", "whale") # ??? Unsure why vowel is long
        # self.assertForm("hræfn", "raven") # ??? Unsure why vowel is long
        self.assertForm("caru", "care")
        self.assertForm("far|an", "fare")
        self.assertForm("stari|an", "stare")

        # E        
        self.assertForm("help|an", "help")
        # self.assertForm("elh", "elk") # The modern word "is not the normal phonetic representative" of the Old English one [OED]
        self.assertForm("tell|an", "tell")
        self.assertForm("betera", "better")
        self.assertForm("streċċ|an", "stretch")
        # self.assertForm("seofon", "seven") # ??? Unsure why vowel is short
        # self.assertForm("myriġ", "merry") # Confusion about form dot space. May want to condense 'iġ' endings
        # self.assertForm("byrġ|an", "bury") # Not based on Anglian dialect. Spelling based on West Saxon, pronunciation based on Kentish
        # self.assertForm("lyft", "left") # Not based on Anglian dialect. Apparently Kentish
        # self.assertForm("cnyll", "knell") # Not based on Anglian dialect. Apparently Kentish
        self.assertForm("cēpte", "kept")
        self.assertForm("mētte", "met")
        # self.assertForm("bēcn|an", "beckon") # ??? 'o' conflicts with 'e' in 'raven'
        # self.assertForm("clǣnsi|an", "cleanse") # Occasional pre-cluster shortening
        # self.assertForm("flǣsċ", "flesh") # Occasional pre-cluster shortening
        # self.assertForm("lǣssa", "less") # Occasional pre-cluster shortening
        self.assertForm("frēond", "friend")
        # self.assertForm("þēofþ", "theft") # ??? Possible 'þ#' -> 't#' change
        self.assertForm("hēold", "held")

        self.assertForm("", "")
        
        # self.assertForm("stel|an", "steal")
        # self.assertFormIn("bāt", ["boat", "bote"])
        # self.assertForm("frēod", "freed")
        # self.assertForm("heofon", "heaven")
        
        # self.assertForm("mete", "meat")
        # self.assertForm("ċild", "child")
        # self.assertForm("dæg", "day")
        # self.assertForm("frēond", "friend")
        # self.assertForm("eorðe", "earth")
        # self.assertForm("cniht", "knight")
        # self.assertForm("mægden", "maiden")
        # self.assertForm("hund", "hound")
        # self.assertForm("bryċġ", "bridge")
        # self.assertForm("gōd", "good")
        # self.assertForm("cēp|an", "keep")
        # self.assertForm("cēpte", "kept")
        # self.assertForm("mēt|an", "meet")
        # self.assertForm("mētte", "met")
        # self.assertForm("niht", "night")
        # self.assertForm("hlæhh|an", "laugh")
        # self.assertForm("tōh", "tough")
        # self.assertForm("nacod", "naked")

    # Helpers ==========

    def assertForm(self, raw, target):
        form = diachronizer.form_from_oe(raw)
        self.assertEqual(form, target)

    def assertFormIn(self, raw, targets):
        form = diachronizer.form_from_oe(raw)
        self.assertIn(form, targets)
        
    def assertFormNot(self, raw, non_target):
        form = diachronizer.form_from_oe(raw)
        self.assertNotEqual(form, non_target)
