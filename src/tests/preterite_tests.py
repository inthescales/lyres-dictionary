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

        return [total, failures]
