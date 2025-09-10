import unittest

import src.evolutor.preterite as preterite

from src.evolutor.engine.config import Config

class PreteriteTests(unittest.TestCase):
    def test_all_preterites(self):
        total = 0
        failures = []
        
        test_set = [
            self._test_preterites
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

    def _test_preterites(self):
        total = 0
        failures = []
        def check(raw, verb_class, target, overrides=[]):
            nonlocal total, failures

            config = Config(verbose=False, locked=True, overrides=overrides)
            form = preterite.oe_form_to_ne_preterite(raw, verb_class, config)
            total += 1
            if not form == target:
                failures.append([form, target])

        # Direct descendents of strong OE preterite -------------------

        # Class 1 — ī

        # Forms with a long 'o' vowel
        check("rīd|an", 1, "rode")
        check("drīf|an", 1, "drove")
        check("sċīn|an", 1, "shone")

        # Forms with a short 'i' vowel
        check("bīt|an", 1, "bit", overrides=[["Pret:class-1-vowel", "i"]])
        check("slīd|an", 1, "slid", overrides=[["Pret:class-1-vowel", "i"]])

        # Class 2

        # As class 4

        # check("frēos|an", 2, "froze") # TODO: Need a way to spell with a 'z' by analogy with lemma
        check("ċēos|an", 2, "chose")
        check("clēof|an", 2, "clove")

        # As class 7

        check("flēog|an", 2, "flew")

        # Class 3 — i + m/n

        check("be-ginn|an", 3, "began")
        check("drinc|an", 3, "drank")
        check("sing|an", 3, "sang")
        check("swimm|an", 3, "swam")

        # -nd ----

        check("find|an", 3, "found")
        check("grind|an", 3, "ground")

        # Class 4 — e + nasal/liquid

        check("ber|an", 4, "bore")
        check("stel|an", 4, "stole")
        check("ter|an", 4, "tore")

        check("brec|an", 4, "broke") # Assimilated from class 5

        # Class 5 — e + other

        check("bidd|an", 5, "bade")
        check("et|an", 5, "ate")
        check("liċġ|an", 5, "lay")

        # Some class 5 verbs use class 4 preterite forms

        check("spec|an", 4, "spoke")
        check("wef|an", 4, "wove")
        # check("tred|an", 4, "trode") # This form was attested as late as the 19th century. Don't know why the vowel is short now.

        # Class 6 — various

        check("drag|an", 6, "drew")
        check("slē|an", 6, "slew")
        check("for-sac|an", 6, "forsook")
        check("sweri|an", 6, "swore")

        # Class 7 — -ow et al.

        # -ow

        check("grōw|an", 7, "grew")
        check("cnāw|an", 7, "knew")

        # contracted in -ōn

        check("h|ōn", 7, "hung")

        # others

        # De-gemination in participles for clasess 5 and 6 -----------------------------

        check("liċġ|an", 5, "lay")

        return [total, failures]
