import unittest

import src.diachronizer.diachronizer as diachronizer

from src.diachronizer.engine.config import Config
from src.diachronizer.engine.environment import Environment

total = 0
failures = []

class DiachronizerTests(unittest.TestCase):
    # def setUp(self)


    def test_form_from_oe(self):
        total = 0
        failures = []
        
        wiki_vowels_total, wiki_vowels_failures = self._test_wiki_vowels()        
        total += wiki_vowels_total
        failures += wiki_vowels_failures

        affix_total, affix_failures = self._test_affixes()
        total +=  affix_total
        failures += affix_failures

        compound_total, compound_failures = self._test_compounds()
        total +=  compound_total
        failures += compound_failures
        
        misc_total, misc_failures = self._test_misc()
        total +=  misc_total
        failures += misc_failures

        print("\n")
        print(str(total) + " words tested, " + str(len(failures))+ " failures:")
        for failure in failures:
            print(str(failure[0]) + " != " + str(failure[1]))

        self.assertEqual(len(failures), 0)

    def _test_wiki_vowels(self):
        total = 0
        failures = []
        def check(raw, target, overrides=[]):
            nonlocal total, failures

            environment = Environment()
            config = Config(verbose=False, locked=True, overrides=overrides)
            form = diachronizer.oe_form_to_ne_form(raw, environment, config)
            total += 1
            if not form == target:
                failures.append([form, target])
        
        # a
        check("mann", "man")
        check("lamb", "lamb")
        check("sang", "sang")
        check("sacc", "sack")
        check("assa", "ass")
        check("fæþm", "fathom")
        check("sæt", "sat")
        check("æt", "at")
        check("mæsse", "mass")
        check("weax", "wax")
        check("healf", "half")
        check("āsci|an", "ask")
        check("fǣtt", "fat")
        check("læst|an", "last")
        # check("blēddre", "bladder")
        check("blǣddre", "bladder", overrides=[["DThA:dər->ðər", False]])
        # check("brēmbel", "bramble")
        check("brǣmbel", "bramble")
        check("swan", "swan")
        check("wasċ|an", "wash")
        check("wann", "wan")
        check("swæþ", "swath")
        check("wæsp", "wasp")
        check("wealwi|an", "wallow")
        check("swealwe", "swallow")
        check("heard", "hard")
        check("ærc", "ark")
        check("swearm", "swarm")
        check("sweart", "swart")
        check("weardi|an", "ward")
        check("wearm", "warm")
        check("wearni|an", "warn")
        check("smæl", "small")
        check("all", "all")
        check("walci|an", "walk")
        # check("ælmesse", "alms")
        check("palm", "palm")
        check("glæs", "glass")
        check("græs", "grass")
        check("pæþ", "path")
        check("æfter", "after")
        
        # a (leng.)
        check("nama", "name")
        check("nacod", "naked")
        check("bac|an", "bake")
        # check("æcer", "acre") # Irregular development due to early borrowing into latin and french
        # check("hwæl", "whale") # ??? Unsure why vowel is long
        # check("hræfn", "raven") # ??? Unsure why vowel is long
        check("caru", "care")
        check("far|an", "fare")
        check("stari|an", "stare")

        # e
        check("help|an", "help")
        # check("elh", "elk") # The modern word "is not the normal phonetic representative" of the Old English one [OED]
        check("tell|an", "tell")
        check("betera", "better")
        check("streċċ|an", "stretch")#{}
        # check("seofon", "seven") # Unsure why vowel is short
        # check("myriġ", "merry") # Confusion about form dot space. May want to condense 'iġ' endings
        check("byrġ|an", "bury", overrides=[["SVC:y->i/e/u", "u"]]) # Not based on Anglian dialect. Spelling based on West Saxon, pronunciation based on Kentish
        check("lyft", "left", overrides=[["SVC:y->i/e/u", "e"]]) # Not based on Anglian dialect. Apparently Kentish
        check("cnyll", "knell", overrides=[["SVC:y->i/e/u", "e"]]) # Not based on Anglian dialect. Apparently Kentish
        check("cēpte", "kept")
        check("mētte", "met")
        # check("bēcn|an", "beckon") # ??? 'o' conflicts with 'e' in 'raven'
        # check("clǣnsi|an", "cleanse") # Occasional pre-cluster shortening
        # check("flǣsċ", "flesh") # Occasional pre-cluster shortening
        # check("lǣssa", "less") # Occasional pre-cluster shortening
        check("frēond", "friend")
        # check("þēofþ", "theft") # ??? Possible 'þ#' -> 't#' change
        # check("hēold", "held") # Depends on 'ld' pre-cluster shortening not applying
        
        # e+r -> ar
        check("heorte", "heart")
        check("berc|an", "bark", overrides=[["Orth:e+r->e/a/ea", "a"]])
        # check("teoru", "tar") # Unsure why vowel is as though short
        check("steorra", "star", overrides=[["Orth:e+r->e/a/ea", "a"]])
        # check("werra", "war", overrides=[["Orth:e+r->e/a/ea", "a"]]) # Anglo-Norman
        # check("werbl|en", "warble", overrides=[["Orth:e+r->e/a/ea", "a"]]) # Not sure if this is OE? Wiki had "AN 'werbler'". Anglo-norman?
        
        # e+r -> er
        check("styrne", "stern", overrides=[["SVC:y->i/e/u", "e"], ["Orth:e+r->e/a/ea", "e"]])
        check("eorl", "earl")
        check("eorþe", "earth")
        check("leorni|an", "learn")
        check("hērde", "heard", overrides=[["PCS:rd", False]])
        
        # e (leng.)
        check("spec|an", "speak")
        check("mete", "meat", overrides=[["Orth:ɛː->ea/eCV", "ea"]])
        check("beofor", "beaver")
        check("meot|an", "mete", overrides=[["Orth:ɛː->ea/eCV", "eCV"]])
        check("eot|an", "eat")
        check("meodu", "mead")
        check("efel", "evil", overrides=[["Orth:ɛː->ea/eCV", "eCV"]])
        check("spere", "spear")
        check("mere", "mere", overrides=[["Orth:ɛː->ea/eCV", "eCV"]])
        check("brec|an", "break")
        check("beor|an", "bear")
        check("pere", "pear")
        check("sweri|an", "swear")
        check("leþer", "leather")
        check("stede", "stead")
        check("weder", "weather", overrides=[["DThA:ðər->dər", True]])
        check("heofon", "heaven")
        check("hefiġ", "heavy")

        # i
        # check("writen", "written") # Might participles be irregularly formed? That is, re-formed in modern morphology by addition of -en
        check("sitt|an", "sit")
        check("fisċ", "fish")
        check("lifer", "liver")
        check("bryċġ", "bridge")
        check("cyss|an", "kiss")
        check("dyde", "did")
        check("synn", "sin")
        check("gyld|an", "gild")
        # check("bysiġ", "busy", overrides=["OSL_iy_false"]) # Not sure how to handle z/s spelling
        # check("wīsdōm", "wisdom") # Will require separate affix handling
        check("fīftiġ", "fifty")
        check("wȳsċ|an", "wish")
        check("cȳþþu", "kith")
        check("fȳst", "fist")
        # check("ċīcen", "chicken") # Test produces wrong result as written, due to the 'occ ī+CV' mentioned in the wiki. Sources are inconsistent with respect to vowel length, though
        # check("lȳtel", "little") # Test produces wrong result as written, due to the 'occ ī+CV' mentioned in the wiki. Sources are inconsistent with respect to vowel length, though
        check("sēoc", "sick", overrides=[["SVC:eːc->ic", True]])
        check("wēoce", "wick", overrides=[["SVC:eːc->ic", True]])
        check("ēc", "ick", overrides=[["SVC:eːc->ic", True]])
        check("gyrd|an", "gird")
        check("fyrst", "first")
        check("styri|an", "stir")
        
        # i (leng.)
        check("wicu", "week", overrides=[["OSL:iy", True]])
        check("pili|an", "peel", overrides=[["OSL:iy", True]])
        # check("bitela", "beetle", overrides=[["OSL:iy", True]]) # "By normal evolution it would be *bittle, but it seems to have been influenced by beetle (n.2)." - etymonline"

        # O
        check("god", "god")
        # check("beġeondan", "beyond") # Will require prefix handling
        # check("gōdspell", "gospel") # May require compound handling. Can't explain dropped 'd'
        check("fōddor", "fodder", overrides=[["DThA:dər->ðər", False]])
        check("fōstri|an", "foster")
        check("moþþe", "moth")
        check("cros", "cross")
        check("frost", "frost")
        check("of", "off")
        check("oft", "oft")
        check("sōfte", "soft")
        check("corn", "corn")
        check("storc", "stork")
        check("storm", "storm")
        
        # O (leng.)
        check("fola", "foal", overrides=[["Orth:ɔː->oa/oCV", "oa"]])
        check("nosu", "nose", overrides=[["Orth:ɔː->oa/oCV", "oCV"]])
        check("ofer", "over", overrides=[["Orth:ɔː->oa/oCV", "oCV"]])
        check("bori|an", "bore", overrides=[["Orth:ɔː->oa/oCV", "oCV"]])
        check("fore", "fore", overrides=[["Orth:ɔː->oa/oCV", "oCV"]])
        # check("bord", "board", overrides=[["PCS:rd", False], ["Orth:ɔː->oa/oCV", "oa"]]) # This is listed as a case of open-syllable lengthening. However come due to homorganic lengthening, the vowel is currently not changing as expected. Should the same stressed vowel changes apply in homorganic lengthening as well?

        # U
        check("bucc", "buck")
        check("lufi|an", "love")
        check("uppe", "up")
        # check("bufan", "above") # Will require prefixes
        # check("myċel", "much") # Inexplicable lost final syllable
        # check("cyċġel", "cudgel", overrides=[["SVC:y->i/e/u", "u"]]) # Not sure about -el ending (cf 'evil')
        check("clyċċ|an", "clutch", overrides=[["SVC:y->i/e/u", "u"]])
        check("sċytel", "shuttle", overrides=[["SVC:y->i/e/u", "u"]])
        # check("dūst", "dust") # Unsure about short vowel. PCS before 'st'?
        check("tūsc", "tusk")
        # check("rūst", "rust") # Unsure about short vowel. PCS before 'st'?
        check("full", "full")
        check("bula", "bull")
        check("bysċ", "bush", overrides=[["SVC:y->i/e/u", "u"]])

        check("spurn|an", "spurn")
        # check("ċyriċe", "church", overrides=[["SVC:y->i/e/u", "u"]]) # Can't explain lost second vowel
        # check("byrþen", "burden", overrides=[["SVC:y->i/e/u", "u"]]) # d/θ alternation without 'd'
        check("hyrdel", "hurdle", overrides=[["SVC:y->i/e/u", "u"]])
        check("word", "word")
        check("werc", "work")
        check("werold", "world")
        check("wyrm", "worm", overrides=[["SVC:y->i/e/u", "u"]])
        check("wersa", "worse")
        check("weorþ", "worth")
        
        # U (leng.)
        # check("guma", "gome", overrides=[["OSL:u", True]) # Not sure about this one
        check("duru", "door", overrides=[["OSL:u", True]])
        check("wudu", "wood", overrides=[["OSL:u", True]])
        
        # Ā
        check("āc", "oak")
        # check("hāl", "whole") # W added to disambiguate from hole
        # check("camb", "comb") # Not sure about pre-cluster shortening. Also need to consider spelling of 'ɔː' before these clusters
        # check("ald", "old") # Not sure about pre-cluster shortening. Also need to consider spelling of 'ɔː' before these clusters
        # check("hald|an", "hold") # Not sure about pre-cluster shortening. Also need to consider spelling of 'ɔː' before these clusters
        check("ār", "oar", overrides=[["Orth:ɔː->oa/oCV", "oa"]])
        check("ār", "ore", overrides=[["Orth:ɔː->oa/oCV", "oCV"]])
        check("māra", "more", overrides=[["Orth:ɔː->oa/oCV", "oCV"]])
        check("bār", "boar")
        check("sār", "sore", overrides=[["Orth:ɔː->oa/oCV", "oCV"]])

        # Ǣ
        check("hǣl|an", "heal")
        check("hǣtu", "heat")
        check("hwǣte", "wheat")
        check("bēat|an", "beat")
        check("lēaf", "leaf")
        check("ċēap", "cheap")
        check("rǣr|an", "rear")
        check("ēare", "ear", overrides=[["Orth:ɛː->ea/eCV", "ea"]])
        check("sēar", "sere", overrides=[["Orth:ɛː->ea/eCV", "eCV"]])
        check("sēari|an", "sear", overrides=[["Orth:ɛː->ea/eCV", "ea"]])        
        check("grēat", "great")
        check("ǣr", "ere", overrides=[["Orth:ɛː->ea/eCV", "eCV"]])
        check("brǣþ", "breath")
        check("swǣt|an", "sweat")
        check("sprǣd|an", "spread")
        check("dēad", "dead")
        check("dēaþ", "death")
        check("þrēat", "threat")
        # check("rēad", "red") # Unsure why vowel is short
        check("dēaf", "deaf")
        check("fēd|an", "feed")
        check("grēdiġ", "greedy")
        # me
        check("fēt", "feet")
        check("dēd", "deed")
        # check("nēdl", "needle") # Unsure why pre-cluster shortening isn't applied
        check("dēop", "deep")
        check("fēond", "fiend")
        # check("betwēonum", "between") # Will need prefix handling
        # be
        check("feld", "field") # Depends on 'ld' pre-cluster shortening
        check("ġeld|an", "yield")
        check("hēr", "here", overrides=[["Orth:ɛː->ea/eCV", "eCV"]])
        check("hēr|an", "hear", overrides=[["Orth:ɛː->ea/eCV", "ea"]])
        check("fēr", "fear")
        check("dēore", "dear")
        check("þēr", "there", overrides=[["Orth:ɛː->ea/eCV", "eCV"]])
        check("hwēr", "where", overrides=[["Orth:ɛː->ea/eCV", "eCV"]])
        check("bēor", "beer", overrides=[["SVC:eːr->ɛːr", False]])
        check("dēor", "deer", overrides=[["SVC:eːr->ɛːr", False]])
        check("stēr|an", "steer", overrides=[["SVC:eːr->ɛːr", False]])
        # check("bēr", "bier") # No known rule for 8['-ier'

        # Ī / Ȳ
        check("rīd|an", "ride")
        check("tīma", "time")
        check("hwīt", "white")
        check("mīn", "mine")
        check("mȳs", "mice")
        check("brȳd", "bride")
        check("hȳd|an", "hide")
        check("find|an", "find")
        check("ċild", "child")
        check("climb|an", "climb")
        check("mynd", "mind")
        check("fȳr", "fire")
        check("hȳri|an", "hire")
        check("wīr", "wire")

        # Ō        
        check("mōna", "moon")
        check("sōna", "soon")
        check("fōd", "food")
        # do
        check("ċēos|an", "choose", overrides=[["SVC:eːo->eː/oː", "oː"]])
        check("sċēot|an", "shoot", overrides=[["SVC:eːo->eː/oː", "oː"]])
        check("flōr", "floor")
        check("mōr", "moor")
        check("blōd", "blood")
        # check("mōdor", "mother", overrides=[["DThA:ðər->dər", True]]) # Can't explain short vowel
        # check("glōfa", "glove") # Unsure why vowel is as if 'ɔː'
        check("gōd", "good")
        check("bōc", "book")
        check("lōci|an", "look")
        check("fōt", "foot")

        # Ū
        check("mūs", "mouse")
        check("ūt", "out")
        check("hlūd", "loud")
        # check("ġefund|en", "found") # Needs prefix handling
        check("hund", "hound")
        # check("ġesund", "sound") # Needs prefix handling
        check("ūre", "our")
        # check("sċūr", "shower") # Produces 'shour', which is accurate to middle english. Unsure about modern spelling
        check("sūr", "sour")
        # check("būtan", "but") # Unsure why vowel is short
        # check("strūti|an", "strut") # Produces 'strout', which reflect middle english 'strouten', but not modern english 'strut'
        
        # Diphthongs
        
        # AI
        check("dæġ", "day")        
        check("mæġ", "may")
        check("mæġden", "maiden")
        check("næġl", "nail")
        check("fæġer", "fair")
        check("clǣġ", "clay")
        check("grǣġ", "gray") # Regular rules produce spelling 'gray'
        check("weġ", "way")
        check("pleġ|an", "play")
        check("reġn", "rain")
        check("leġer", "layer", overrides=[["Orth:aiV->ai/ay", "ay"]])
        check("leġde", "laid")
        check("hēġ", "hay")

        # Ī
        # check("ēage", "eye") # Possibly idiosincratic. Same question about the palatalization of the 'g' as the below 
        check("lēġ|an", "lie", overrides=[["Orth:iː#->ie/ye", "ie"]]) # Sources show the modern word as originating from 'lēogan'. 'lēġan' is a later form. Not able to generate the modern form from the original due to the non-palatal 'g', but the intermediary form works.
        check("flēġe", "fly") # Sources show the modern word is originating from 'flēoge'. This form is an assumed intermediate stage based on the above. I don't know when the 'g' became palatalized
        check("tiġel", "tile")
        check("liġe", "lie", overrides=[["Orth:iː#->ie/ye", "ie"]])
        check("hīġi|an", "hie", overrides=[["Orth:iː#->ie/ye", "ie"]])
        check("ryġe", "rye", overrides=[["Orth:iː#->ie/ye", "ye"]])
        check("byġe", "buy", overrides=[["SVC:y->i/e/u", "u"]])
        check("drȳġe", "dry")
        
        # AU
        check("clawu", "claw")
        check("lagu", "law")
        check("drag|an", "draw")

        # ɛu
        check("mǣw", "mew", overrides=[["Orth:ɛ/iu->ew/ue", "ew"]])
        check("lǣwede", "lewd", overrides=[["Orth:ɛ/iu->ew/ue", "ew"]])
        check("sċrēawa", "shrew", overrides=[["Orth:ɛ/iu->ew/ue", "ew"]])
        check("dēaw", "dew", overrides=[["Orth:ɛ/iu->ew/ue", "ew"]])
        check("ċēow|an", "chew", overrides=[["Orth:ɛ/iu->ew/ue", "ew"]])
        check("hrēow|an", "rue", overrides=[["Orth:ɛ/iu->ew/ue", "ue"]])
        check("trēwe", "true", overrides=[["Orth:ɛ/iu->ew/ue", "ue"]]) # Source had the west saxon 'trīewe'. This is my guess at an Anglian form
        # check("Tiwesdæġ", "Tuesday") # Needs compound handling

        # ɔu
        check("cnāw|an", "know")
        check("crāwa", "crow")
        check("snāw", "snow")
        check("sāwol", "soul")
        # check("āg|an", "owe")# Idiosyncratic?
        check("grōw|an", "grow")
        check("blōwen", "blown")
        check("boga", "bow")
        check("flogen", "flown")

        
        # Ū
        # check("fugol", "fowl") # Current process produces 'foul'. Need more examples to understand this
        # check("drugaþ", "drought")  # Idiosyncratic. Normal rules would produce 'drout'

        check("būg|an", "bow")

        # auh
        check("slæhtor", "slaughter")
        check("hlæhtor", "laughter")

        # ɛih
        check("streht", "straight")

        # i:h
        check("hēh", "high")
        check("þēh", "thigh")
        check("nēh", "nigh")
        check("riht", "right")
        check("flyht", "flight")
        check("līht", "light")

        # ɔuh
        check("dāg", "dough")
        check("trog", "trough")
        
        # uːh
        check("bōg", "bough")
        check("plōg", "plough")

        # check("ġenōg", "enough") # Probably needs prefix handling
        check("tōh", "tough")
        check("ruh", "rough")
        
        return [total, failures]

    def _test_affixes(self):
        total = 0
        failures = []
        def check(raw, target, overrides=[]):
            nonlocal total, failures

            environment = Environment()
            config = Config(verbose=False, locked=True, overrides=overrides)
            form = diachronizer.oe_form_to_ne_form(raw, environment, config)
            total += 1
            if not form == target:
                failures.append([form, target])

        check("", "")

        return [total, failures]
        
    def _test_compounds(self):
        total = 0
        failures = []
        def check(raw, target, overrides=[]):
            nonlocal total, failures

            environment = Environment()
            config = Config(verbose=False, locked=True, overrides=overrides)
            form = diachronizer.oe_form_to_ne_form(raw, environment, config)
            total += 1
            if not form == target:
                failures.append([form, target])

        check("ǣfen-tīd", "eventide", overrides=[["Orth:ɛː->ea/eCV", "eCV"]])
        check("ealdor-mann", "alderman", overrides=[["DThA:dər->ðər", False]])
        check("gold-smið", "goldsmith")
        check("sǣ-mann", "seaman")
        check("sunn-bēam", "sunbeam")
        check("beru-scinn", "bearskin")
        
        # Difficult cases
        # check("god-spel", "gospel") # Needs special handling for 'd-s' compound joining, maybe
        # check("god-sibb", "gossip") # Can't explain 'b' -> 'p'
        # check("gos-hafoc", "goshawk") # Can't explain 'hafoc' -> 'hawk'
        # check("hand-ġeweorc", "handiwork") # Needs prefix handling, and an exception case
        # Handiwork as above
        # check("nēah-ġebur", "neighbor") # Not sure how to make this work
        # check("twī-feald", "twofold") # Can't explain the 'o' in 'two'
        # check("gat-hyrde", "goatherd", overrides=[["SVC:y->i/e/u", "e"]]) # The development of 'goat' is confusing
        # check("gar-leac", "garlic") # Can't explain final '-ic' spelling

        return [total, failures]
    
    def _test_misc(self):
        total = 0
        failures = []
        def check(raw, target, overrides=[]):
            nonlocal total, failures

            environment = Environment()
            config = Config(verbose=False, locked=True, overrides=overrides)
            form = diachronizer.oe_form_to_ne_form(raw, environment, config)
            total += 1
            if not form == target:
                failures.append([form, target])
        
        check("stel|an", "steal")
        check("bāt", "boat", overrides=[["Orth:ɔː->oa/oCV", "oa"]])
        check("frēod", "freed")
        check("heofon", "heaven")
        
        check("mete", "meat")
        check("ċild", "child")
        check("dæġ", "day")
        check("frēond", "friend")
        check("eorðe", "earth")
        check("cniht", "knight")
        check("mæġden", "maiden")
        check("hund", "hound")
        check("gōd", "good")
        check("cēp|an", "keep")
        check("cēpte", "kept")
        check("mēt|an", "meet")
        check("mētte", "met")
        check("niht", "night")
        check("hlæhh|an", "laugh")
        check("tōh", "tough")
        check("nacod", "naked")
    
        return [total, failures]
    
    # Helpers ==========

    def check_equal(self, raw, target, config):
        form = diachronizer.form_from_oe(raw, config)
        return form == target
    
    def check_in(self, raw, targets, config):
        global total, failures
        form = diachronizer.form_from_oe(raw, config)
        
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
