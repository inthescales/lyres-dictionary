import unittest

import src.evolutor.evolutor as evolutor

from src.evolutor.engine.config import Config

class PastParticipleTests(unittest.TestCase):
    def test_all_past_participles(self):
        total = 0
        failures = []
        
        test_set = [
            self._test_past_participles
        ]
        
        for test in test_set:
            test_total, test_failures = test()
            total += test_total
            failures += test_failures

        if len(failures) > 0:
            print("\n")
            print(str(total) + " words tested, " + str(len(failures))+ " failures:")
            for failure in failures:
                print(str(failure[0]) + " != " + str(failure[1]))

        self.assertEqual(len(failures), 0)

    def _test_past_participles(self):
        total = 0
        failures = []
        def check(raw, verb_class, target, overrides=[]):
            nonlocal total, failures

            config = Config(verbose=False, locked=True, overrides=overrides)
            form = evolutor.oe_form_to_ne_participle(raw, verb_class, config)
            total += 1
            if not form == target:
                failures.append([form, target])

        # Direct descendents of strong OE participle -------------------

        # Class 1 — ī
        check("bīt|an", 1, "bitten")
        check("rīd|an", 1, "ridden")
        check("wrīt|an", 1, "written")

        # Class 2 — ēo
        check("ċēos|an", 2, "chosen", overrides=[["SVC:eːo->eː/oː", "oː"]])
        check("clēof|an", 2, "cloven")
        check("flēog|an", 2, "flown")
        check("frēos|an", 2, "frosen") # TODO: Figure out if there's a way to retain the 'z' here

        # Class 3

        # Class 3 strong verbs usually drop the '-en' suffix

        check("grind|an", 3, "ground")
        check("wind|an", 3, "wound")
        check("feoht|an", 3, "fought")
        check("ġield|an", 3, "yold")

        # But in a few forms they keep it.

        check("drinc|an", 3, "drunken", overrides=[["PPart:use-class-3-suffix", True]])
        check("sċrinc|an", 3, "shrunken", overrides=[["PPart:use-class-3-suffix", True]])
        check("sinc|an", 3, "sunken", overrides=[["PPart:use-class-3-suffix", True]])
        check("feoht|an", 3, "foughten", overrides=[["PPart:use-class-3-suffix", True]])
        check("swell|an", 3, "swollen", overrides=[["PPart:use-class-3-suffix", True]])

        # Class 4

        check("ber|an", 4, "born")
        check("brec|an", 4, "broken")
        check("stel|an", 4, "stolen")

        # Class 5

        # Class 5 participle forms are highly irregular in PDE

        # A few act predictably

        check("et|an", 5, "eaten")
        check("cweþ|an", 5, "queathen")

        # Some take class 4 style participles

        check("spec|an", 4, "spoken")
        check("wef|an", 4, "woven")

        # Others I don't know how to account for

        # check("bidd|an", 5, "bidden")
        # check("tred|an", 5, "trodden")
        # check("sitt|an", 5, "sitten") # Appears irregular

        # Class 6

        check("for-sac|an", 6, "forsaken")
        check("sċeac|an", 6, "shaken")
        check("slē|an", 6, "slain")
        # check("sweri|an", 6, "sworn") # FIX THIS

        # Class 7

        # Of type 1 (ending in '-ow')

        check("blāw|an", 7, "blown")
        check("grōw|an", 7, "grown")
        check("cnāw|an", 7, "known")

        # Of type 2 (all others)

        check("bēat|an", 7, "beaten")
        check("feall|an", 7, "fallen")
        check("hēaw|an", 7, "hewn", overrides=[["Orth:ɛ/iu->ew/ue", "ew"]])

        # Direct descendants of weak OE verb participles ------------------------

        # Weak
        check("bend|an", "weak", "bended")
        check("send|an", "weak", "sended")
        check("stōwi|an", "weak", "stowed")

        # Strong OE verbs treated as weak — modern form + '-ed' ending ----------

        # Strong class 1
        check("glīd|an", 1, "glided", overrides=[["PPart:use-strong", False]])
        check("spīw|an", 1, "spewed", overrides=[["PPart:use-strong", False], ["Orth:ɛ/iu->ew/ue", "ew"]])
        check("wriþ|an", 1, "writhed", overrides=[["PPart:use-strong", False]])

        # Strong class 2
        check("brēow|an", 2, "brewed", overrides=[["PPart:use-strong", False], ["Orth:ɛ/iu->ew/ue", "ew"]])
        check("lēog|an", 2, "lied", overrides=[["PPart:use-strong", False]])
        check("sēoþ|an", 2, "seethed", overrides=[["PPart:use-strong", False]])

        # Strong class 3
        check("beorc|an", 3, "barked", overrides=[["PPart:use-strong", False], ["Orth:e+r->e/a/ea", "a"]])
        check("sweorf|an", 3, "swerved", overrides=[["PPart:use-strong", False], ["Orth:e+r->e/a/ea", "e"]])
        check("delf|an", 3, "delved", overrides=[["PPart:use-strong", False]])
        check("ġell|an", 3, "yelled", overrides=[["PPart:use-strong", False]])
        check("help|an", 3, "helped", overrides=[["PPart:use-strong", False]])
        check("spurn|an", 3, "spurned", overrides=[["PPart:use-strong", False]])

        # Strong class 4

        # Few class 4 verbs use weak participles in PDE.

        check("cwel|an", 4, "quealed", overrides=[["PPart:use-strong", False]])
        check("nim|an", 4, "nimmed", overrides=[["PPart:use-strong", False]])

        # Strong class 5

        check("cned|an", 5, "kneaded", overrides=[["PPart:use-strong", False]])
        check("met|an", 5, "meted", overrides=[["PPart:use-strong", False], ["Orth:ɛː->ea/eCV", "eCV"]])
        check("wrec|an", 5, "wreaked", overrides=[["PPart:use-strong", False]])

        # Strong class 6
        check("stepp|an", 6, "stepped", overrides=[["PPart:use-strong", False]])
        check("wasċ|an", 6, "washed", overrides=[["PPart:use-strong", False]])
        check("hlæhh|an", 6, "laughed", overrides=[["PPart:use-strong", False]])

        # Strong class 7
        check("drǣd|an", 7, "dreaded", overrides=[["PPart:use-strong", False]])
        check("gang|an", 7, "ganged", overrides=[["PPart:use-strong", False], ["HL:ng", False]])
        check("hlēap|an", 7, "leaped", overrides=[["PPart:use-strong", False]])

        # Weak participle forms, with contraction --------------------------------------

        # TODO: Add contracted weak participle forms

        # '-t' suffix (often with shortened vowel in pronunciation, but unchanged spelling)
        # 'leap' -> 'leapt'
        # 'dream' -> 'dreamt'
        # 'laugh' -> 'laught'
        # 'mean' -> 'meant'

        # Shortened vowel with '-t' suffix
        # 'keep' -> 'kept'
        # 'sleep' -> 'slept'
        # 'weep' -> 'wept'

        # '-l' -> '-lt'
        # 'spill' -> 'spilt'
        # 'spoil' -> 'spoilt'

        # '-n' -> '-nt'
        # 'burn' -> 'burnt'

        # '-nd' -> 'nt'
        # 'bend' -> 'bent'
        # 'lend' -> 'lent'
        # 'rend' -> 'rent'

        # Participles with Verner's Law changes ----------------------------------------

        # TODO: Add Verner's Law support to strong participle forms
        
        # 'forlese' -> 'forlorn'
        # 'freeze' -> 'froren'

        # Participles for contracted verbs ---------------------------------------------

        check("tē|on", "weak", "teed")
        check("wrē|on", 1, "wrine") #* Conjectured form, taken from Anglish wiki
        check("flē|on", 2, "flown")
        check("h|ōn", 7, "hangen")
        check("f|ōn", 7, "fanged", overrides=[["PPart:use-strong", False]])

        return [total, failures]