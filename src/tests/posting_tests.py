import unittest

from src.generation.generator import word_for_keys
from src.morphs.morphothec import Morphothec
from src.posting import posting

class PostingTests(unittest.TestCase):
    def setUp(self):
        self.morphothec = Morphothec("data/")

    # Tests that posts with sexual roots will have content warnings
    def testWarnSexualContent(self):
        self.assertWarned(["phallos", "-ic"], True)
        self.assertWarned(["hǣman", "-ere"], True)
        self.assertWarned(["pintel", "-lēas"], True)

        self.assertWarned(["canis", "-al"], False)
        self.assertWarned(["femina", "-ify"], False)
        self.assertWarned(["arktos", "-ic"], False)
        self.assertWarned(["athlein", "-sis"], False)
        self.assertWarned(["gyltan", "-ere"], False)
        self.assertWarned(["gold", "-lēas"], False)

    # Helpers ==========
    
    def assertWarned(self, keys, warned):
        word = word_for_keys(keys, self.morphothec)
        meta = posting.get_meta(word)
        is_warned = "warning" in meta and len("warning") > 0
        self.assertEqual(is_warned, warned)

if __name__ == '__main__':    
    unittest.main()