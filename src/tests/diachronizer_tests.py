import unittest

import src.diachronizer.diachronizer as diachronizer

from src.diachronizer.engine.config import Config

total = 0
failures = []

class DiachronizerTests(unittest.TestCase):
    # def setUp(self)


    def test_form_from_oe(self):
        total = 0
        failures = []
        
        test_set = [
            self._test_wiki_vowels,
            self._test_affixes,
            self._test_compounds,
            self._test_homorganic_lengthening,
            self._test_unstressed_vowel_spelling,
            self._test_misc
        ]
        
        for test in test_set:
            test_total, test_failures = test()
            total += test_total
            failures += test_failures

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

            config = Config(verbose=False, locked=True, overrides=overrides)
            form = diachronizer.oe_form_to_ne_form(raw, config)
            total += 1
            if not form == target:
                failures.append([form, target])
        
        # a
        check("mann", "man")
        # check("lamb", "lamb") # Seems to be irregular - would expect 'lomb', analogous to 'camb' -> 'comb', due to homorganic lengthening
        check("sang", "sang", overrides=[["HL:ng", False]])
        check("sacc", "sack")
        check("assa", "ass")
        check("fæþm", "fathom")
        check("sæt", "sat")
        check("æt", "at")
        check("mæsse", "mass")
        check("weax", "wax")
        check("healf", "half")
        # check("āsci|an", "ask") # OED suggests irregularity - would expect 'osk', with 'aː' being changed to 'ɔː', then shortened to 'ɔ'
        check("fǣtt", "fat")
        check("læst|an", "last")
        check("blǣddre", "bladder", overrides=[["DThA:dər->ðər", False]]) # List used different form
        check("brǣmbel", "bramble") # List used different form
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
        # check("ælmesse", "alms") # Not sure how to make this work. Maybe misparsed as plural
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
        # check("hwæl", "whale") # OED: "The present form whale represents oblique forms (Old English hwalas, etc.). TODO: simulate this?"
        check("hræfn", "raven") # Unsure why vowel is long, but additional spelling rules compensate
        check("caru", "care")
        check("far|an", "fare")
        check("stari|an", "stare")

        # e
        check("help|an", "help")
        # check("elh", "elk") # The modern word "is not the normal phonetic representative" of the Old English one [OED]
        check("tell|an", "tell")
        check("betera", "better")
        check("streċċ|an", "stretch")#{}
        check("seofon", "seven", overrides=[["Orth:ɛː->ea/eCV", "eCV"]]) # Unsure why vowel is short, but spelling is plausible
        # check("myriġ", "merry") # Confusion about form. May be influence by history as affixed root
        check("byrġ|an", "bury", overrides=[["SVC:y->i/e/u", "u"]]) # Not based on Anglian dialect. Spelling based on West Saxon, pronunciation based on Kentish
        check("lyft", "left", overrides=[["SVC:y->i/e/u", "e"]]) # Not based on Anglian dialect. Apparently Kentish
        check("cnyll", "knell", overrides=[["SVC:y->i/e/u", "e"]]) # Not based on Anglian dialect. Apparently Kentish
        check("cēpte", "kept")
        check("mētte", "met")
        # check("bēcn|an", "beckon") # ??? 'o' conflicts with 'e' in 'raven'. TODO: try the idea I wrote down
        # check("clǣnsi|an", "cleanse") # OED: "The modern spelling cleanse seems to be artificial, assimilated to clean"
        check("flǣsċ", "flesh", overrides=[["PCS:ɛː->a", False]])
        check("lǣssa", "less", overrides=[["PCS:ɛː->a", False]])
        check("frēond", "friend")
        # check("þēofþ", "theft") # ??? Possible 'þ#' -> 't#' change
        check("heold", "held") # Wiki has 'hēold', but 'heold' seems attested
        
        # e+r -> ar
        check("heorte", "heart")
        check("berc|an", "bark", overrides=[["Orth:e+r->e/a/ea", "a"]])
        # check("teoru", "tar") # Unsure why vowel is short
        check("steorra", "star", overrides=[["Orth:e+r->e/a/ea", "a"]])
        
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
        # check("writen", "written") # System wants '-on' ending. This word is excepted as a participle
        check("sitt|an", "sit")
        check("fisċ", "fish")
        check("lifer", "liver")
        check("bryċġ", "bridge")
        check("cyss|an", "kiss")
        check("dyde", "did")
        check("synn", "sin")
        check("gyld|an", "gild")
        check("bysiġ", "busy", overrides=[["SVC:y->i/e/u", "u"], ["OSL:iy", False]])
        # check("wīsdōm", "wisdom") # Will require separate affix handling
        check("fīftiġ", "fifty")
        check("wȳsċ|an", "wish")
        check("cȳþþu", "kith")
        check("fȳst", "fist")
        # check("ċīcen", "chicken") # Appears to be irregular vowel shortening
        check("lyttel", "little") # Chart had form 'lȳtel', which seems to be more standard, but may not be the actual ancestor here
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
        # check("be-ġeond", "beyond") # Not sure about vowel
        # check("gōd-spell", "gospel") # Can't explain dropped 'd' or the short 'o'
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
        check("bord", "board", overrides=[["PCS:rd", False], ["Orth:ɔː->oa/oCV", "oa"]])

        # U
        check("bucc", "buck")
        check("lufi|an", "love")
        check("uppe", "up")
        check("a-bufa", "above") # List had 'abufan'. Removing final-n seems normal in this cases, as in beġeondan
        # check("myċel", "much") # Irregular loss of final syllable. Wiktionary: "apocopated variant of muchel"
        # check("cyċġel", "cudgel", overrides=[["SVC:y->i/e/u", "u"]]) # Need to sort out -el spelling (cf 'evil')
        check("clyċċ|an", "clutch", overrides=[["SVC:y->i/e/u", "u"]])
        check("sċytel", "shuttle", overrides=[["SVC:y->i/e/u", "u"]])
        check("dust", "dust") # List had 'dūst', but OE 'dust' is hypothesized. ME shows derivations of both forms.
        check("tūsc", "tusk")
        check("rust", "rust") # List had 'rūst', but OE 'rust' is also attested. ME shows derivations of both forms.
        check("full", "full")
        check("bula", "bull")
        check("bysċ", "bush", overrides=[["SVC:y->i/e/u", "u"]])

        check("spurn|an", "spurn")
        # check("ċyriċe", "church", overrides=[["SVC:y->i/e/u", "u"]]) # Can't explain loss of second vowel
        # check("byrþen", "burden", overrides=[["SVC:y->i/e/u", "u"]]) # d/θ alternation without 'r'
        check("hyrdel", "hurdle", overrides=[["SVC:y->i/e/u", "u"]])
        check("word", "word")
        check("werc", "work")
        check("werold", "world")
        check("wyrm", "worm", overrides=[["SVC:y->i/e/u", "u"]])
        check("wersa", "worse")
        check("weorþ", "worth")
        
        # U (leng.)
        # check("guma", "gome", overrides=[["OSL:u", True]) # Not sure about spelling. 'goom' seems regular
        check("duru", "door", overrides=[["OSL:u", True]])
        check("wudu", "wood", overrides=[["OSL:u", True]])
        
        # Ā
        check("āc", "oak")
        # check("hāl", "whole") # W added to disambiguate from hole
        check("camb", "comb")
        check("ald", "old")
        check("hald|an", "hold")
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
        # check("rēad", "red") # Long 'ɛ' before 'd' will be shortened in early modern English. Modern spelling reflects this change, but words like 'stead' and 'dead' do not
        check("dēaf", "deaf")
        check("fēd|an", "feed")
        check("grēdiġ", "greedy")
        # me
        check("fēt", "feet")
        check("dēd", "deed")
        # check("nēdl", "needle") # Irregular. Wiktionary: the final vowel is generalised from the Old English oblique cases. 
        check("dēop", "deep")
        check("fēond", "fiend")
        check("be-twēonum", "between") # List had 'betwēonum'. Tweaked for the sake of test.
        # be
        check("feld", "field")
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
        # check("bēr", "bier") # Irregular. OED: The modern spelling (since 1600) appears to be due to imitation of the French form bière

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
        check("mōdor", "mother", overrides=[["DThA:ðər->dər", True]]) # Can't explain short vowel
        # check("glōfa", "glove") # Unsure why vowel is as if 'ɔː'
        check("gōd", "good")
        check("bōc", "book")
        check("lōci|an", "look")
        check("fōt", "foot")

        # Ū
        check("mūs", "mouse")
        check("ūt", "out")
        check("hlūd", "loud")
        check("ġe|fund|en", "found") # Needs prefix handling
        check("hund", "hound")
        check("ġe|sund", "sound") # Needs prefix handling
        check("ūre", "our")
        # check("sċūr", "shower") # Produces 'shour', which is accurate to middle english. Unsure about modern spelling
        check("sūr", "sour")
        # check("būtan", "but") # Unsure why vowel is short
        # check("strūti|an", "strut") # Produces 'strout', which reflect middle english 'strout', but not modern english 'strut'
        
        # Diphthongs
        
        # AI
        check("dæġ", "day")        
        check("mæġ", "may")
        check("mæġden", "maiden", overrides=[["Orth:ə->o", False]])
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
        # check("ēage", "eye") # Palatalized in oblique form.
            # OED: "In Old English usually a weak neuter (ēage).
            # Although not shown by the spelling, the original velar consonant would have undergone palatalization in the nominative and
            # accusative singular (before a front vowel) while remaining unchanged elsewhere"
            # Also: "the standard spelling eye comes from varieties where the long ē was not raised)""
        check("lēoġ|an", "lie", overrides=[["Orth:iː#->ie/ye", "ie"]]) # List has 'leogan'. It seems the 'g' was palatalized at some point, but I'm not sure when.
        check("flēoġe", "fly") # List has 'fleogan'. It seems the 'g' was palatalized at some point, but I'm not sure when.
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
        check("trēwe", "true", overrides=[["Orth:ɛ/iu->ew/ue", "ue"]]) # List had West Saxon 'trīewe'. Anglian smoothing would produce 'trēwe' instead
        # check("Tiwes-dæġ", "Tuesday") # The 's' is doubled according to usual rules. As a compound possessive I suspect this is irregular

        # ɔu
        check("cnāw|an", "know")
        check("crāwa", "crow")
        check("snāw", "snow")
        check("sāwol", "soul")
        # check("āg|an", "owe")# Spelling is likely idiosyncratic. Regular rules produce 'ow'.
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

        # check("ġe|nōg", "enough") # Needs possibility for prefix to take vowel form
        check("tōh", "tough")
        check("ruh", "rough")
        
        return [total, failures]

    def _test_affixes(self):
        total = 0
        failures = []
        def check(raw, target, overrides=[]):
            nonlocal total, failures

            config = Config(verbose=False, locked=True, overrides=overrides)
            form = diachronizer.oe_form_to_ne_form(raw, config)
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

            config = Config(verbose=False, locked=True, overrides=overrides)
            form = diachronizer.oe_form_to_ne_form(raw, config)
            total += 1
            if not form == target:
                failures.append([form, target])

        check("ǣfen-tīd", "eventide", overrides=[["Orth:ɛː->ea/eCV", "eCV"]])
        check("ealdor-mann", "alderman", overrides=[["DThA:dər->ðər", False]])
        check("gold-smið", "goldsmith")
        check("sǣ-mann", "seaman")
        check("sunn-bēam", "sunbeam")
        check("beru-scinn", "bearskin")

        return [total, failures]
    
    def _test_misc(self):
        total = 0
        failures = []
        def check(raw, target, overrides=[]):
            nonlocal total, failures

            config = Config(verbose=False, locked=True, overrides=overrides)
            form = diachronizer.oe_form_to_ne_form(raw, config)
            total += 1
            if not form == target:
                failures.append([form, target])
        
        check("bāt", "boat", overrides=[["Orth:ɔː->oa/oCV", "oa"]])
        check("cēp|an", "keep")
        check("cēpte", "kept")
        check("ċild", "child")
        check("cniht", "knight")
        check("dæġ", "day")
        check("eorðe", "earth")
        check("frēod", "freed")
        check("frēond", "friend")
        check("gōd", "good")
        check("īs", "ice")
        check("heofon", "heaven")
        check("hlæhh|an", "laugh")
        check("hund", "hound")
        check("mæġden", "maiden", overrides=[["Orth:ə->o", False]])
        check("mete", "meat")
        check("mēt|an", "meet")
        check("mētte", "met")
        check("niht", "night")
        check("nacod", "naked")
        check("stel|an", "steal")
        check("tōh", "tough")

        # -ō[d/ð]er -> -o[d/ð]er
        check("brōþor", "brother")

        # final '-e' for words ending in voiced fricatives
        check("ċēos|an", "choose", overrides=[["SVC:eːo->eː/oː", "oː"]])

        # Non-affix -iġ forms
        check("bysiġ", "busy", overrides=[["SVC:y->i/e/u", "u"]])
        check("ċeariġ", "chary")
        check("dohtiġ", "doughty")
        check("drēoriġ", "dreary")
        check("dysiġ", "dizzy")
        check("hāliġ", "holy", overrides=[["Orth:ɔː->oa/oCV", "oCV"]])
        check("hefiġ", "heavy")
    
        return [total, failures]

    # Tests for homorganic lengthening, and related pre-cluster shortening and vowel changes
    def _test_homorganic_lengthening(self):
        total = 0
        failures = []
        def check(raw, target, overrides=[]):
            nonlocal total, failures

            config = Config(verbose=False, locked=True, overrides=overrides)
            form = diachronizer.oe_form_to_ne_form(raw, config)
            total += 1
            if not form == target:
                failures.append([form, target])
        
        # ng ---------------------

        # stressed a becomes o, in most cases
        check("lang", "long")
        check("strang", "strong")
        check("wrang", "wrong")
        check("mangere", "monger")

        # ...but there are a couple exceptions
        check("gang", "gang", overrides=[["HL:ng", False]])
        check("sang", "sang", overrides=[["HL:ng", False]])

        # other vowels are unaffected
        check("hring|an", "ring")
        check("sing|an", "sing")
        check("sting|an", "sting")

        return [total, failures]

    # Tests related to the vowel used to spell unstressed vowels (i.e. /ə/)
    def _test_unstressed_vowel_spelling(self):
        total = 0
        failures = []
        def check(raw, target, overrides=[]):
            nonlocal total, failures

            config = Config(verbose=False, locked=True, overrides=overrides)
            form = diachronizer.oe_form_to_ne_form(raw, config)
            total += 1
            if not form == target:
                failures.append([form, target])
        
        # In most cases, /ə/ is spelled with an 'e'
        check("feþer", "feather")

        # Words with a final nasal use 'o' in most cases
        check("bēacn", "beacon")
        check("becn|an", "beckon")
        check("wǣpn", "weapon")

        check("besmā", "besom")
        check("bosm", "bosom") # Should be 'bōsm', but that produces a long vowel and I can't find a reason. Good enough for this test.
        check("fæþm", "fathom")

        # ...but it seems a preceding 'v' changes it
        check("hræfn", "raven")

        # ... I think we want to leave it if there's a non-digraphic long vowel in the preceding syllable
        check("open", "open")

        # ...and there are a few other exceptions
        check("glædene", "gladdon", overrides=[["Orth:ə->o", True]])
        check("mæġden", "maiden", overrides=[["Orth:ə->o", False]])

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
