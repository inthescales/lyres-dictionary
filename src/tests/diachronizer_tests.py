import unittest

import diachronizer as diachronizer

total = 0
failures = []

class DiachronizerTests(unittest.TestCase):
    # def setUp(self)
    
    def testFormFromOE(self):
        
        # a
        self.test_equal("mann", "man")
        self.test_equal("lamb", "lamb")
        self.test_equal("sang", "sang")
        self.test_equal("sacc", "sack")
        self.test_equal("assa", "ass")
        self.test_equal("fæþm", "fathom")
        self.test_equal("sæt", "sat")
        self.test_equal("æt", "at")
        self.test_equal("mæsse", "mass")
        self.test_equal("weax", "wax")
        self.test_equal("healf", "half")
        self.test_equal("āsci|an", "ask")
        self.test_equal("fǣtt", "fat")
        self.test_equal("læst|an", "last")
        # self.test_equal("blēddre", "bladder")
        self.test_equal("blǣddre", "bladder")
        # self.test_equal("brēmbel", "bramble")
        self.test_equal("brǣmbel", "bramble")
        self.test_equal("swan", "swan")
        self.test_equal("wasċ|an", "wash")
        self.test_equal("wann", "wan")
        self.test_equal("swæþ", "swath")
        self.test_equal("wæsp", "wasp")
        self.test_equal("wealwi|an", "wallow")
        self.test_equal("swealwe", "swallow")
        self.test_equal("heard", "hard")
        self.test_equal("ærc", "ark")
        self.test_equal("swearm", "swarm")
        self.test_equal("sweart", "swart")
        self.test_equal("weardi|an", "ward")
        self.test_equal("wearm", "warm")
        self.test_equal("wearni|an", "warn")
        self.test_equal("smæl", "small")
        self.test_equal("all", "all")
        self.test_equal("walci|an", "walk")
        # self.test_equal("ælmesse", "alms")
        self.test_equal("palm", "palm")
        self.test_equal("glæs", "glass")
        self.test_equal("græs", "grass")
        self.test_equal("pæþ", "path")
        self.test_equal("æfter", "after")
        
        # a (leng.)
        self.test_equal("nama", "name")
        self.test_equal("nacod", "naked")
        self.test_equal("bac|an", "bake")
        # self.test_equal("æcer", "acre") # Irregular development due to early borrowing into latin and french
        # self.test_equal("hwæl", "whale") # ??? Unsure why vowel is long
        # self.test_equal("hræfn", "raven") # ??? Unsure why vowel is long
        self.test_equal("caru", "care")
        self.test_equal("far|an", "fare")
        self.test_equal("stari|an", "stare")

        # e
        self.test_equal("help|an", "help")
        # self.test_equal("elh", "elk") # The modern word "is not the normal phonetic representative" of the Old English one [OED]
        self.test_equal("tell|an", "tell")
        self.test_equal("betera", "better")
        self.test_equal("streċċ|an", "stretch")
        # self.test_equal("seofon", "seven") # ??? Unsure why vowel is short
        # self.test_equal("myriġ", "merry") # Confusion about form dot space. May want to condense 'iġ' endings
        # self.test_equal("byrġ|an", "bury") # Not based on Anglian dialect. Spelling based on West Saxon, pronunciation based on Kentish
        # self.test_equal("lyft", "left") # Not based on Anglian dialect. Apparently Kentish
        # self.test_equal("cnyll", "knell") # Not based on Anglian dialect. Apparently Kentish
        self.test_equal("cēpte", "kept")
        self.test_equal("mētte", "met")
        # self.test_equal("bēcn|an", "beckon") # ??? 'o' conflicts with 'e' in 'raven'
        # self.test_equal("clǣnsi|an", "cleanse") # Occasional pre-cluster shortening
        # self.test_equal("flǣsċ", "flesh") # Occasional pre-cluster shortening
        # self.test_equal("lǣssa", "less") # Occasional pre-cluster shortening
        self.test_equal("frēond", "friend")
        # self.test_equal("þēofþ", "theft") # ??? Possible 'þ#' -> 't#' change
        self.test_equal("hēold", "held")
        
        # e+r -> ar
        self.test_equal("heorte", "heart")
        self.test_equal("berc|an", "bark")
        self.test_equal("teoru", "tar")
        self.test_equal("steorra", "star")
        self.test_equal("werra", "war")
        self.test_equal("werbl|en", "warble")
        
        # e+ -> er
        self.test_equal("sterne", "stern")
        self.test_equal("eorl", "earl")
        self.test_equal("eorþe", "earth")
        self.test_equal("leorni|an", "learn")
        self.test_equal("hērde", "heard")
        
        # e (leng.)
        self.test_equal("spec|an", "speak")
        self.test_in("mete", ["meat", "mete"])
        self.test_equal("beofor", "beaver")
        self.test_in("meot|an", ["mete", "meat"])
        self.test_equal("eot|an", "eat")
        self.test_equal("meodu", "mead")
        self.test_equal("yfel", "evil")
        self.test_equal("spere", "spear")
        self.test_equal("mere", "mere")
        self.test_equal("brec|an", "break")
        self.test_equal("beor|an", "bear")
        self.test_equal("pere", "pear")
        self.test_equal("sweri|an", "swear")
        self.test_equal("leþer", "leather")
        self.test_equal("stede", "stead")
        self.test_equal("weder", "weather")
        self.test_equal("heofon", "heaven")
        self.test_equal("hefiġ", "heavy")

        self.test_equal("", "")
        
        # self.test_equal("stel|an", "steal")
        # self.test_equalIn("bāt", ["boat", "bote"])
        # self.test_equal("frēod", "freed")
        # self.test_equal("heofon", "heaven")
        
        # self.test_equal("mete", "meat")
        # self.test_equal("ċild", "child")
        # self.test_equal("dæg", "day")
        # self.test_equal("frēond", "friend")
        # self.test_equal("eorðe", "earth")
        # self.test_equal("cniht", "knight")
        # self.test_equal("mægden", "maiden")
        # self.test_equal("hund", "hound")
        # self.test_equal("bryċġ", "bridge")
        # self.test_equal("gōd", "good")
        # self.test_equal("cēp|an", "keep")
        # self.test_equal("cēpte", "kept")
        # self.test_equal("mēt|an", "meet")
        # self.test_equal("mētte", "met")
        # self.test_equal("niht", "night")
        # self.test_equal("hlæhh|an", "laugh")
        # self.test_equal("tōh", "tough")
        # self.test_equal("nacod", "naked")

        print("=== Test finished ===")
        print(str(total) + " words tested, " + str(len(failures))+ " failures:")
        for failure in failures:
            print(str(failure[0]) + " != " + str(failure[1]))
        
    # Helpers ==========

    def test_equal(self, raw, target):
        global total, failures
        form = diachronizer.form_from_oe(raw)
        
        if form != target:
            failures.append([form, target])
        total += 1

        return form == target
    
    def test_in(self, raw, targets):
        global total, failures
        form = diachronizer.form_from_oe(raw)
        
        if form not in targets:
            failures.append([form, targets])
        total += 1

        return form in targets

    def assertForm(self, raw, target):
        form = diachronizer.form_from_oe(raw)
        self.assertEqual(form, target)

    def assertFormIn(self, raw, targets):
        form = diachronizer.form_from_oe(raw)
        self.assertEqual(form, targets)
        
    def assertFormNot(self, raw, non_target):
        form = diachronizer.form_from_oe(raw)
        self.assertEqual(form, non_target)
