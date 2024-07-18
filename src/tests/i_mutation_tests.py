import unittest

import src.evolutor.evolutor as evolutor
import src.evolutor.language.oe_phonology as oe_phonology

from src.evolutor.engine.config import Config

total = 0
failures = []

# NOTE ========================================================

# These tests test the i-mutation process as well as affixes and transforms that assert i-mutation.
# As it stands, some of these tests fail. While I have some basic code for applying i-mutation to a word,
# I haven't been able to find a satisfactory way to use it.
#
# Some reasons include:
# - I'm not currently creating inflected forms (as in plurals like 'mouse' -> 'mice')
# - I don't think I could come up with good glosses for verbs formed this way (as in 'moot' -> 'meet' and 'food' -> 'feed')
# - The feminine '-en' suffix (as in 'vixen' and OE 'gyden') seem to use a pre-OE form of i-mutation that doesn't match
#   the i-mutation vowel changes observed in OE. Because of this, I'm not sure I can reasonably use it without adding a
#   proto-germanic module (there may be a way to hack it, but I'm not attempting now)
#     - That said, OE 'wylfen', 'elfen' do match my the i-mutation schemas on Wikipedia, so maybe that represents an intra-OE
#       usage of this suffix that I could simulate?
# - The main other use case, the -th suffix (as in 'length' and 'breadth') feels difficult to pin down — some of the vowel
#   changes feel difficult to explain (for instance, the vowel shortens in 'deep' -> 'depth', but not in 'broad' -> 'breadth').
#   And there aren't many instances, so it's difficult to establish a secure pattern.
#     - I did implement a quick version of combined sound processing, so that vowels could be shortened by the extra final consonant.
#       It mostly did work as expected, but also caused new problems (e.g. words with final schwas didn't drop them).
#       But also, it didn't produce -th forms that consistently match actual examples.
#       I have not kept this code
#
# These tests stand as a record of what I was able to accomplish, and a reminder of the difficulties I encountered.
# Maybe it will be possible to do something here in the future.

# The second block of tests is now disabled as I've removed i-mutation handling from the evolution/generation code.
# To make it work again, add an environment (if I haven't added one yet) to the evolution code, and invoke the code
# in the i-mutation file as part of the generation process.

# ==============================================================

class IMutationTests(unittest.TestCase):
    def test_i_mutation(self):
        total = 0
        failures = []
        
        test_set = [
            self._test_oe_i_mutation# ,
            # self._test_diachronic_i_mutation # DISABLED, see above
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

    # Tests for i-mutation within Old English
    def _test_oe_i_mutation(self):
        total = 0
        failures = []
        def check_oe(raw, target, overrides=[]):
            nonlocal total, failures

            form = oe_phonology.get_i_mutated_word(raw, "mercian")
            total += 1
            if not form == target:
                failures.append([form, target])

        # Plural nouns
        # check_oe("bōc", "bēċ") # Would need to add palatalization
        check_oe("man", "men")
        check_oe("mūs", "mȳs")
        check_oe("tōþ", "tēþ")

        # Verbs 

        return [total, failures]

    # Tests for i-mutation going from OE to MnE
    def _test_diachronic_i_mutation(self):
        total = 0
        failures = []
        def check_mne(raw, target, suffix=None, overrides=[]):
            nonlocal total, failures

            config = Config(verbose=False, locked=True, overrides=overrides)
            form = evolutor.oe_form_to_ne_form(raw, config)
            if suffix != None:
                form += suffix

            total += 1
            if not form == target:
                failures.append([form, target])

        def check_mne_th(raw, target, suffix=None, overrides=[]):
            return check_mne(raw, target, suffix="th", overrides=[])

        # Plural nouns
        check_mne("man", "men")
        check_mne("mūs", "mice")
        check_mne("tōþ", "teeth")

        # Nouns in -th

        # a -> ɛ
        check_mne_th("lang", "length")
        check_mne_th("strang", "strength")
        check_mne_th("wrang", "wrength")

        # aː -> ɛː
        check_mne_th("brād", "breadth")
        check_mne_th("hāl", "health")

        # eːo -> ɛ
        check_mne_th("dēop", "depth") # Needs joining to shorten vowel
        check_mne_th("hlēow", "lewth")

        # i -> i
        check_mne_th("mild", "milth") # Need some new rule to drop 'd'
        check_mne_th("stille", "stilth") # Needs joining to avoid duplicate 'l'

        # iːC -> i
        check_mne_th("wīd", "width") # Needs joining to shorten vowel

        # ???
        check_mne_th("slāw", "sloth")
        check_mne_th("wele", "wealth")
        
        # Verbs in -th

        check_mne_th("hyċġ|an", "highth")
        check_mne_th("grōw|an", "growth")
        check_mne_th("hreow|an", "ruth") # Needs joining to simplify vowel spelling
        check_mne_th("tili|an", "tilth") # Needs joining to avoid duplicate 'l'

        # Verbs in -jan
        
        check_mne("full", "fill")
        check_mne("hāl", "heal")
        check_mne("fōd", "feed")
        check_mne("mōt", "meet")

        return [total, failures]
