import unittest

import src.utils.helpers as helpers

class HelperTests(unittest.TestCase):
    
    def testVowelsAndConsonants(self):
        for char in ["a", "e", "i", "o", "u"]:
            self.assertTrue(helpers.is_vowel(char))
            self.assertFalse(helpers.is_consonant(char))

        for char in ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y"]:
            self.assertFalse(helpers.is_vowel(char))
            self.assertTrue(helpers.is_consonant(char))

        self.assertTrue(helpers.is_vowel("y", True))
        self.assertFalse(helpers.is_vowel("y", False))
        self.assertFalse(helpers.is_vowel("y", False))
        self.assertTrue(helpers.is_vowel("y", True))

        self.assertFalse(helpers.y_is_vowel_heuristic(None))
        self.assertFalse(helpers.y_is_vowel_heuristic("a"))
        self.assertTrue(helpers.y_is_vowel_heuristic("t"))
        self.assertTrue(helpers.y_is_vowel_heuristic("y"))

    def testSyllables(self):
        self.assertEqual(helpers.syllable_count("flea"), 1)
        self.assertEqual(helpers.syllable_count("old"), 1)
        self.assertEqual(helpers.syllable_count("warm"), 1)

        self.assertEqual(helpers.syllable_count("echo"), 2)
        self.assertEqual(helpers.syllable_count("magnum"), 2)
        self.assertEqual(helpers.syllable_count("smile"), 2) #*

        self.assertEqual(helpers.syllable_count("rubicon"), 3)
        self.assertEqual(helpers.syllable_count("simile"), 3)

        self.assertEqual(helpers.syllable_count("panopticon"), 4)

    def testSplitClusters(self):
        def is_vowel(letter):
            return letter in ["a", "e", "i", "o", "u"]

        self.assertEqual(helpers.split_clusters("assess", lambda char: is_vowel(char)), ["a", "ss", "e", "ss"])
        self.assertEqual(helpers.split_clusters("scarecrow", lambda char: is_vowel(char)), ["sc", "a", "r", "e", "cr", "o", "w"])
        self.assertEqual(helpers.split_clusters("yarrow", lambda char: is_vowel(char)), ["y", "a", "rr", "o", "w"])

        def is_vowel_oe(letter):
            return letter in ["æ", "ǣ", "a", "ā", "e", "ē", "i", "ī", "o", "ō", "u", "ū", "y", "ȳ"]

        self.assertEqual(helpers.split_clusters("ċeorfan", lambda char: is_vowel_oe(char)), ["ċ", "eo", "rf", "a", "n"])
        self.assertEqual(helpers.split_clusters("snytru", lambda char: is_vowel_oe(char)), ["sn", "y", "tr", "u"])

    def testArticles(self):
        self.assertEqual(helpers.indefinite_article_for("cat"), "a")
        self.assertEqual(helpers.indefinite_article_for("worm"), "a")
        self.assertEqual(helpers.indefinite_article_for("yell"), "a")

        self.assertEqual(helpers.indefinite_article_for("entity"), "an")
        self.assertEqual(helpers.indefinite_article_for("ogre"), "an")
        self.assertEqual(helpers.indefinite_article_for("urge"), "an")

    def testMisc(self):
        self.assertTrue(helpers.l_in_last_two("alea"))
        self.assertTrue(helpers.l_in_last_two("vel"))
        self.assertTrue(helpers.l_in_last_two("avuncul"))
        self.assertTrue(helpers.l_in_last_two("tubul"))

        self.assertFalse(helpers.l_in_last_two("caten"))
        self.assertFalse(helpers.l_in_last_two("ventr"))

        self.assertTrue(helpers.l_in_last_two("leg"))

        self.assertFalse(helpers.l_in_last_two("liter"))

if __name__ == '__main__':    
    unittest.main()