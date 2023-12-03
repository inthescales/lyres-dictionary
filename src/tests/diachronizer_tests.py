import unittest

import diachronizer as diachronizer

total = 0
failures = []

class DiachronizerTests(unittest.TestCase):
    # def setUp(self)
    
    def testFormFromOE(self):
        
        # a
        self.check_equal("mann", "man")
        self.check_equal("lamb", "lamb")
        self.check_equal("sang", "sang")
        self.check_equal("sacc", "sack")
        self.check_equal("assa", "ass")
        self.check_equal("fæþm", "fathom")
        self.check_equal("sæt", "sat")
        self.check_equal("æt", "at")
        self.check_equal("mæsse", "mass")
        self.check_equal("weax", "wax")
        self.check_equal("healf", "half")
        self.check_equal("āsci|an", "ask")
        self.check_equal("fǣtt", "fat")
        self.check_equal("læst|an", "last")
        # self.check_equal("blēddre", "bladder")
        self.check_equal("blǣddre", "bladder")
        # self.check_equal("brēmbel", "bramble")
        self.check_equal("brǣmbel", "bramble")
        self.check_equal("swan", "swan")
        self.check_equal("wasċ|an", "wash")
        self.check_equal("wann", "wan")
        self.check_equal("swæþ", "swath")
        self.check_equal("wæsp", "wasp")
        self.check_equal("wealwi|an", "wallow")
        self.check_equal("swealwe", "swallow")
        self.check_equal("heard", "hard")
        self.check_equal("ærc", "ark")
        self.check_equal("swearm", "swarm")
        self.check_equal("sweart", "swart")
        self.check_equal("weardi|an", "ward")
        self.check_equal("wearm", "warm")
        self.check_equal("wearni|an", "warn")
        self.check_equal("smæl", "small")
        self.check_equal("all", "all")
        self.check_equal("walci|an", "walk")
        # self.check_equal("ælmesse", "alms")
        self.check_equal("palm", "palm")
        self.check_equal("glæs", "glass")
        self.check_equal("græs", "grass")
        self.check_equal("pæþ", "path")
        self.check_equal("æfter", "after")
        
        # a (leng.)
        self.check_equal("nama", "name")
        self.check_equal("nacod", "naked")
        self.check_equal("bac|an", "bake")
        # self.check_equal("æcer", "acre") # Irregular development due to early borrowing into latin and french
        # self.check_equal("hwæl", "whale") # ??? Unsure why vowel is long
        # self.check_equal("hræfn", "raven") # ??? Unsure why vowel is long
        self.check_equal("caru", "care")
        self.check_equal("far|an", "fare")
        self.check_equal("stari|an", "stare")

        # e
        self.check_equal("help|an", "help")
        # self.check_equal("elh", "elk") # The modern word "is not the normal phonetic representative" of the Old English one [OED]
        self.check_equal("tell|an", "tell")
        self.check_equal("betera", "better")
        self.check_equal("streċċ|an", "stretch")#{}
        # self.check_equal("seofon", "seven") # Unsure why vowel is short
        # self.check_equal("myriġ", "merry") # Confusion about form dot space. May want to condense 'iġ' endings
        # self.check_equal("byrġ|an", "bury") # Not based on Anglian dialect. Spelling based on West Saxon, pronunciation based on Kentish
        # self.check_equal("lyft", "left") # Not based on Anglian dialect. Apparently Kentish
        # self.check_equal("cnyll", "knell") # Not based on Anglian dialect. Apparently Kentish
        self.check_equal("cēpte", "kept")
        self.check_equal("mētte", "met")
        # self.check_equal("bēcn|an", "beckon") # ??? 'o' conflicts with 'e' in 'raven'
        # self.check_equal("clǣnsi|an", "cleanse") # Occasional pre-cluster shortening
        # self.check_equal("flǣsċ", "flesh") # Occasional pre-cluster shortening
        # self.check_equal("lǣssa", "less") # Occasional pre-cluster shortening
        self.check_equal("frēond", "friend")
        # self.check_equal("þēofþ", "theft") # ??? Possible 'þ#' -> 't#' change
        self.check_equal("hēold", "held")
        
        # e+r -> ar
        self.check_equal("heorte", "heart")
        self.check_equal("berc|an", "bark", overrides=["orth_e+r->a"])
        # self.check_equal("teoru", "tar") # Unsure why vowel is as though short
        self.check_equal("steorra", "star", overrides=["orth_e+r->a"])
        self.check_equal("werra", "war", overrides=["orth_e+r->a"])
        self.check_equal("werbl|en", "warble", overrides=["orth_e+r->a"])
        
        # e+ -> er
        self.check_equal("sterne", "stern", overrides=["orth_e+r->e"])
        self.check_equal("eorl", "earl")
        self.check_equal("eorþe", "earth")
        self.check_equal("leorni|an", "learn")
        self.check_equal("hērde", "heard")
        
        # e (leng.)
        self.check_equal("spec|an", "speak")
        self.check_equal("mete", "meat", overrides=["orth_ɛː->ea"])
        self.check_equal("beofor", "beaver")
        self.check_equal("meot|an", "mete", overrides=["orth_ɛː->eCV"])
        self.check_equal("eot|an", "eat")
        self.check_equal("meodu", "mead")
        self.check_equal("efel", "evil", overrides=["orth_ɛː->eCV"])
        self.check_equal("spere", "spear")
        self.check_equal("mere", "mere", overrides=["orth_ɛː->eCV"])
        self.check_equal("brec|an", "break")
        self.check_equal("beor|an", "bear")
        self.check_equal("pere", "pear")
        self.check_equal("sweri|an", "swear")
        self.check_equal("leþer", "leather")
        self.check_equal("stede", "stead")
        # self.check_equal("weder", "weather") # No handling for 'd' -> 'th' yet
        self.check_equal("heofon", "heaven")
        self.check_equal("hefiġ", "heavy")

        # i
        # self.check_equal("writen", "written") # Might participles be irregularly formed? That is, re-formed in modern morphology by addition of -en
        self.check_equal("sitt|an", "sit")
        self.check_equal("fisċ", "fish")
        self.check_equal("lifer", "liver", overrides=["OSL_iy_false"])
        self.check_equal("bryċġ", "bridge")
        self.check_equal("cyss|an", "kiss")
        # self.check_equal("dyde", "did")
        self.check_equal("synn", "sin")
        self.check_equal("gyld|an", "gild")
        # self.check_equal("bysiġ", "busy", overrides=["OSL_iy_false"]) # Not sure how to handle z/s spelling
        # self.check_equal("wīsdōm", "wisdom") # Will require separate affix handling
        self.check_equal("fīftiġ", "fifty")
        self.check_equal("wȳsċ|an", "wish")
        self.check_equal("cȳþþu", "kith")
        self.check_equal("fȳst", "fist")
        # self.check_equal("ċīcen", "chicken") # occ ī+CV
        # self.check_equal("lȳtel", "little") # occ ȳ+CV
        # self.check_equal("sēoc", "sick") # occ ēoc
        # self.check_equal("wēoce", "wick") # occ #eoc
        # self.check_equal("ēc", "eke") # occ ēc
        self.check_equal("gyrd|an", "gird")
        self.check_equal("fyrst", "first")
        self.check_equal("styri|an", "stir", overrides=["OSL_iy_false"])
        
        # i (leng.)
        self.check_equal("wicu", "week", overrides=["OSL_iy_true"])
        self.check_equal("pili|an", "peel", overrides=["OSL_iy_true"])
        # self.check_equal("bitela", "beetle", overrides=["OSL_iy_true"]) # "By normal evolution it would be *bittle, but it seems to have been influenced by beetle (n.2)." - etymonline"

        # O
        self.check_equal("god", "god")
        # self.check_equal("beġeondan", "beyond") # Will require prefix handling
        # self.check_equal("gōdspell", "gospel") # May require compound handling. Can't explain dropped 'd'
        self.check_equal("fōddor", "fodder")
        self.check_equal("fōstri|an", "foster")
        self.check_equal("moþþe", "moth")
        self.check_equal("cros", "cross")
        self.check_equal("frost", "frost")
        self.check_equal("of", "off")
        self.check_equal("oft", "oft")
        self.check_equal("sōfte", "soft")
        self.check_equal("corn", "corn")
        self.check_equal("storc", "stork")
        self.check_equal("storm", "storm")
        
        # O (leng.)
        self.check_equal("fola", "foal", overrides=["orth_ɔː->oa"])
        self.check_equal("nosu", "nose", overrides=["orth_ɔː->oCV"])
        self.check_equal("ofer", "over", overrides=["orth_ɔː->oCV"])
        self.check_equal("bori|an", "bore", overrides=["orth_ɔː->oCV"])
        self.check_equal("fore", "fore", overrides=["orth_ɔː->oCV"])
        # self.check_equal("bord", "board") # Needs 'rd' homorganic lengthening


        self.check_equal("", "")
        
        # self.check_equal("stel|an", "steal")
        # self.check_equalIn("bāt", ["boat", "bote"])
        # self.check_equal("frēod", "freed")
        # self.check_equal("heofon", "heaven")
        
        # self.check_equal("mete", "meat")
        # self.check_equal("ċild", "child")
        # self.check_equal("dæg", "day")
        # self.check_equal("frēond", "friend")
        # self.check_equal("eorðe", "earth")
        # self.check_equal("cniht", "knight")
        # self.check_equal("mægden", "maiden")
        # self.check_equal("hund", "hound")
        # self.check_equal("gōd", "good")
        # self.check_equal("cēp|an", "keep")
        # self.check_equal("cēpte", "kept")
        # self.check_equal("mēt|an", "meet")
        # self.check_equal("mētte", "met")
        # self.check_equal("niht", "night")
        # self.check_equal("hlæhh|an", "laugh")
        # self.check_equal("tōh", "tough")
        # self.check_equal("nacod", "naked")

        print("=== Test finished ===")
        print(str(total) + " words tested, " + str(len(failures))+ " failures:")
        for failure in failures:
            print(str(failure[0]) + " != " + str(failure[1]))
        
    # Helpers ==========

    def check_equal(self, raw, target, overrides=[]):
        global total, failures
        form = diachronizer.form_from_oe(raw, overrides)
        
        if form != target:
            failures.append([form, target])
        total += 1

        return form == target
    
    def check_in(self, raw, targets, overrides=[]):
        global total, failures
        form = diachronizer.form_from_oe(raw, overrides)
        
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
