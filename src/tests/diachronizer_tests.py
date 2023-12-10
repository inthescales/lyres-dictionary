import unittest

import diachronizer as diachronizer

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

            form = diachronizer.form_from_oe(raw, overrides)
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
        check("blǣddre", "bladder")
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
        # check("byrġ|an", "bury") # Not based on Anglian dialect. Spelling based on West Saxon, pronunciation based on Kentish
        # check("lyft", "left") # Not based on Anglian dialect. Apparently Kentish
        # check("cnyll", "knell") # Not based on Anglian dialect. Apparently Kentish
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
        check("berc|an", "bark", overrides=["orth_e+r->a"])
        # check("teoru", "tar") # Unsure why vowel is as though short
        check("steorra", "star", overrides=["orth_e+r->a"])
        check("werra", "war", overrides=["orth_e+r->a"])
        # check("werbl|en", "warble", overrides=["orth_e+r->a"]) # Not sure if this is OE? Wiki had "AN 'werbler'". Anglo-norman?
        
        # e+r -> er
        check("styrne", "stern", overrides=["y->e", "orth_e+r->e"])
        check("eorl", "earl")
        check("eorþe", "earth")
        check("leorni|an", "learn")
        # check("hērde", "heard") # Depends on 'rd' not being pre-cluster shortened
        
        # e (leng.)
        check("spec|an", "speak")
        check("mete", "meat", overrides=["orth_ɛː->ea"])
        check("beofor", "beaver")
        check("meot|an", "mete", overrides=["orth_ɛː->eCV"])
        check("eot|an", "eat")
        check("meodu", "mead")
        check("efel", "evil", overrides=["orth_ɛː->eCV"])
        check("spere", "spear")
        check("mere", "mere", overrides=["orth_ɛː->eCV"])
        check("brec|an", "break")
        check("beor|an", "bear")
        check("pere", "pear")
        check("sweri|an", "swear")
        check("leþer", "leather")
        check("stede", "stead")
        # check("weder", "weather") # No handling for 'd' -> 'th' yet
        check("heofon", "heaven")
        check("hefiġ", "heavy")

        # i
        # check("writen", "written") # Might participles be irregularly formed? That is, re-formed in modern morphology by addition of -en
        check("sitt|an", "sit")
        check("fisċ", "fish")
        check("lifer", "liver", overrides=["OSL_iy_false"])
        check("bryċġ", "bridge")
        check("cyss|an", "kiss")
        # check("dyde", "did")
        check("synn", "sin")
        check("gyld|an", "gild")
        # check("bysiġ", "busy", overrides=["OSL_iy_false"]) # Not sure how to handle z/s spelling
        # check("wīsdōm", "wisdom") # Will require separate affix handling
        check("fīftiġ", "fifty")
        check("wȳsċ|an", "wish")
        check("cȳþþu", "kith")
        check("fȳst", "fist")
        # check("ċīcen", "chicken") # Test produces wrong result as written, do to the 'occ ī+CV' mentioned in the wiki. Sources are inconsistent with respect to vowel length, though
        # check("lȳtel", "little") # Test produces wrong result as written, do to the 'occ ī+CV' mentioned in the wiki. Sources are inconsistent with respect to vowel length, though
        check("sēoc", "sick", overrides=["eːc->ic_true"])
        check("wēoce", "wick", overrides=["eːc->ic_true"])
        check("ēc", "ick", overrides=["eːc->ic_true"])
        check("gyrd|an", "gird")
        check("fyrst", "first")
        check("styri|an", "stir", overrides=["OSL_iy_false"])
        
        # i (leng.)
        check("wicu", "week", overrides=["OSL_iy_true"])
        check("pili|an", "peel", overrides=["OSL_iy_true"])
        # check("bitela", "beetle", overrides=["OSL_iy_true"]) # "By normal evolution it would be *bittle, but it seems to have been influenced by beetle (n.2)." - etymonline"

        # O
        check("god", "god")
        # check("beġeondan", "beyond") # Will require prefix handling
        # check("gōdspell", "gospel") # May require compound handling. Can't explain dropped 'd'
        check("fōddor", "fodder")
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
        check("fola", "foal", overrides=["orth_ɔː->oa"])
        check("nosu", "nose", overrides=["orth_ɔː->oCV"])
        check("ofer", "over", overrides=["orth_ɔː->oCV"])
        check("bori|an", "bore", overrides=["orth_ɔː->oCV"])
        check("fore", "fore", overrides=["orth_ɔː->oCV"])
        # check("bord", "board") # Needs 'rd' homorganic lengthening

        # U
        check("bucc", "buck")
        check("lufi|an", "love", overrides=["OSL_u_false"])
        check("uppe", "up")
        # check("bufan", "above") # Will require prefixes
        # check("myċel", "much") # Inexplicable lost final syllable
        # check("cyċġel", "cudgel", overrides=["y->u"]) # Not sure about -el ending (cf 'evil')
        check("clyċċ|an", "clutch", overrides=["y->u"])
        check("sċytel", "shuttle", overrides=["y->u"])
        # check("dūst", "dust") # Unsure about short vowel. PCS before 'st'?
        check("tūsc", "tusk")
        # check("rūst", "rust") # Unsure about short vowel. PCS before 'st'?
        check("full", "full")
        check("bula", "bull")
        check("bysċ", "bush", overrides=["y->u"])

        check("spurn|an", "spurn")
        # check("ċyriċe", "church", overrides=["y->u"]) # Can't explain lost second vowel
        # check("byrþen", "burden", overrides=["y->u"]) # d/θ alternation
        check("hyrdel", "hurdle", overrides=["y->u"])
        check("word", "word")
        check("werc", "work")
        check("werold", "world")
        check("wyrm", "worm", overrides=["y->u"])
        check("wersa", "worse")
        check("weorþ", "worth")
        
        # U (leng.)
        # check("guma", "gome", overrides=["OSL_u_true"]) # Not sure about this one
        check("duru", "door", overrides=["OSL_u_true"])
        check("wudu", "wood", overrides=["OSL_u_true"])
        
        # Ā
        check("āc", "oak")
        # check("hāl", "whole") # W added to disambiguate from hole
        # check("camb", "comb") # Not sure about pre-cluster shortening. Also need to consider spelling of 'ɔː' before these clusters
        # check("ald", "old") # Not sure about pre-cluster shortening. Also need to consider spelling of 'ɔː' before these clusters
        # check("hald|an", "hold") # Not sure about pre-cluster shortening. Also need to consider spelling of 'ɔː' before these clusters
        self.check_in("ār", ["oar", "1re"])
        check("māra", "more", overrides=["orth_ɔː->oCV"])
        check("bār", "boar")
        check("sār", "sore", overrides=["orth_ɔː->oCV"])

        # Ǣ
        check("hǣl|an", "heal")
        check("hǣtu", "heat")
        check("hwǣte", "wheat")
        check("bēat|an", "beat")
        check("lēaf", "leaf")
        check("ċēap", "cheap")
        check("rǣr|an", "rear")
        check("ēare", "ear", overrides=["orth_ɛː->ea"])
        check("sēar", "sere", overrides=["orth_ɛː->eCV"])
        check("sēari|an", "sear", overrides=["orth_ɛː->ea"])        
        check("grēat", "great")
        check("ǣr", "ere", overrides=["orth_ɛː->eCV"])
        check("brǣþ", "breath")
        check("swǣt|an", "sweat")
        check("sprǣd|an", "spread")
        check("dēad", "dead")
        check("dēaþ", "death")
        check("þrēat", "threat")
        # check("rēad", "red") # Unsure why vowel is shortm
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
        check("hēr", "here", overrides=["orth_ɛː->eCV"])
        check("hēr|an", "hear", overrides=["orth_ɛː->ea"])
        check("fēr", "fear")
        check("dēore", "dear")
        check("þēr", "there", overrides=["orth_ɛː->eCV"])
        check("hwēr", "where", overrides=["orth_ɛː->eCV"])
        check("bēor", "beer", overrides=["eːr->ɛːr_false"])
        check("dēor", "deer", overrides=["eːr->ɛːr_false"])
        check("stēr|an", "steer", overrides=["eːr->ɛːr_false"])
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
        check("ċēos|an", "choose", overrides=["eːo->oː"])
        check("sċēot|an", "shoot", overrides=["eːo->oː"])
        check("flōr", "floor")
        check("mōr", "moor")
        check("blōd", "blood")
        # check("mōdor", "mother") # Needs 'd'/'ð' alternation
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
        # check("sċūr", "shower") # Produces 'scour', which is accurate to middle english. Unsure about modern spelling
        check("sūr", "sour")
        # check("būtan", "but") # Unsure why vowel is short
        # check("strūti|an", "strut") # Produces 'strout', which reflect middle english 'strouten', but not modern english 'strut'
        
        # Diphthongs
        
        # AI
        check("dæġ", "day")        
        check("mæġ", "may")
        check("mæġden", "maiden")
        check("næġl", "nail")
        check("fæġer", "fair", overrides=["aiV->ai"])
        check("clǣġ", "clay")
        check("grǣġ", "gray") # Regular rules produce spelling 'gray'
        check("weġ", "way")
        check("pleġ|an", "play")
        check("reġn", "rain")
        check("leġer", "layer", overrides=["aiV->ay"])
        check("leġde", "laid")
        check("hēġ", "hay")

        # Ī
        # check("ēage", "eye") # Possibly idiosincratic. Same question about the palatalization of the 'g' as the below 
        check("lēġ|an", "lie", overrides=["iː#->ie#"]) # Sources show the modern word as originating from 'lēogan'. 'lēġan' is a later form. Not able to generate the modern form from the original due to the non-palatal 'g', but the intermediary form works.
        check("flēġe", "fly") # Sources show the modern word is originating from 'flēoge'. This form is an assumed intermediate stage based on the above. I don't know when the 'g' became palatalized
        check("tiġel", "tile")
        check("liġe", "lie", overrides=["iː#->ie#"])
        check("hīġi|an", "hie", overrides=["iː#->ie#"])
        check("ryġe", "rye", overrides=["iː#->ye#"])
        check("byġe", "buy", overrides=["y->u"])
        check("drȳġe", "dry")
        
        # AU
        check("clawu", "claw")
        check("lagu", "law")
        check("drag|an", "draw")

        # ɛu
        check("mǣw", "mew", overrides=["ɛ/iu->ew"])
        check("lǣwede", "lewd", overrides=["ɛ/iu->ew"])
        check("sċrēawa", "shrew", overrides=["ɛ/iu->ew"])
        check("dēaw", "dew", overrides=["ɛ/iu->ew"])
        check("ċēow|an", "chew", overrides=["ɛ/iu->ew"])
        check("hrēow|an", "rue", overrides=["ɛ/iu->ue"])
        check("trēwe", "true", overrides=["ɛ/iu->ue"]) # Source had the west saxon 'trīewe'. This is my guess at an Anglian form
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
        
    def _test_misc(self):
        total = 0
        failures = []
        def check(raw, target, overrides=[]):
            nonlocal total, failures

            form = diachronizer.form_from_oe(raw, overrides)
            total += 1
            if not form == target:
                failures.append([form, target])
        
        check("stel|an", "steal")
        check("bāt", "boat", overrides=["orth_ɔː->oa"])
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

    def check_equal(self, raw, target, overrides=[]):
        form = diachronizer.form_from_oe(raw, overrides)
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
