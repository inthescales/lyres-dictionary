import unittest

import diachronizer as diachronizer

class DiachronizerTests(unittest.TestCase):
    # def setUp(self):

    def testFormFromOE(self):
        self.assertForm("stel|an", "steal")
        self.assertFormIn("bāt", ["boat", "bote"])
        self.assertForm("frēod", "freed")
        self.assertForm("heofon", "heaven")
        self.assertForm("mete", "meat")
        self.assertForm("ċild", "child")
        self.assertForm("dæg", "day")
        self.assertForm("frēond", "friend")
        self.assertForm("nama", "name")
        self.assertForm("eorðe", "earth")
        self.assertForm("cniht", "knight")
        self.assertForm("mægden", "maiden")
        self.assertForm("hund", "hound")
        self.assertForm("bryċġ", "bridge")
        self.assertForm("gōd", "good")
        self.assertForm("cēp|an", "keep")
        self.assertForm("cēpte", "kept")
        self.assertForm("mēt|an", "meet")
        self.assertForm("mētte", "met")
        self.assertForm("niht", "night")
        self.assertForm("hlæhh|an", "laugh")
        self.assertForm("tōh", "tough")
        self.assertForm("mann", "man")
        self.assertFormNot("lamb", "lamb")
        self.assertForm("nacod", "naked")

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
