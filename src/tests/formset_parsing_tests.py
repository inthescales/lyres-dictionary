import unittest

import src.generation.forming.mne_formset as mne_formset
import src.generation.forming.oe_formset as oe_formset

class FormsetParsingTests(unittest.TestCase):
    def test_oe_formsets(self):
        from_string = oe_formset.read("form", "noun")
        self.assertEqual(from_string.main.paradigm.lemma, "form")
        self.assertEqual(from_string.alt, None)

        from_string_list = oe_formset.read(["first", "second"], "noun")
        self.assertEqual([p.lemma for p in from_string_list.main.paradigm], ["first", "second"])

        from_paradigm = oe_formset.read({ "lemma": "lem", "oblique": "ob"}, "noun")
        self.assertEqual([from_paradigm.main.paradigm.lemma, from_paradigm.main.paradigm.oblique], ["lem", "ob"])

        from_paradigm_list = oe_formset.read([{ "lemma": "first"}, { "lemma": "second" }], "noun")
        self.assertEqual([p.lemma for p in from_paradigm_list.main.paradigm], ["first", "second"])

    def test_oe_multiform(self):
        string = oe_formset.read_multiform({"main": "mainform", "alt": "altform" }, "noun")
        self.assertEqual([string.main.paradigm.lemma] + [p.lemma for p in [a.paradigm for a in string.alt]], ["mainform", "altform"])

        string_list = oe_formset.read_multiform({"main": "mainform", "alt": ["firstalt", "secondalt"] }, "noun")
        self.assertEqual([string_list.main.paradigm.lemma] + [p.lemma for p in [a.paradigm for a in string_list.alt]], ["mainform", "firstalt", "secondalt"])

    def test_oe_metaforms(self):
        one_string = oe_formset.read_metaform("form", "noun")
        self.assertEqual(one_string.paradigm.lemma, "form")

        string_list = oe_formset.read_metaform(["first", "second"], "noun")
        self.assertEqual([p.lemma for p in string_list.paradigm], ["first", "second"])

        one_paradigm = oe_formset.read_metaform({ "lemma": "form" }, "noun")
        self.assertEqual(one_paradigm.paradigm.lemma, "form")

        paradigm_list = oe_formset.read_metaform([{ "lemma": "first" }, { "lemma": "second" }], "noun")
        self.assertEqual([p.lemma for p in paradigm_list.paradigm], ["first", "second"])

        full_dict = oe_formset.read_metaform({ "form": "form", "canon": "canon", "dialect": "anglian" }, "noun")
        self.assertEqual([full_dict.paradigm.lemma, full_dict.canon.paradigm.lemma, full_dict.dialect], ["form", "canon", "anglian"])

    def test_oe_canonset(self):
        from_string = oe_formset.read_canonset("form", "noun")
        self.assertEqual(from_string.paradigm.lemma, "form")

        from_string_list = oe_formset.read_canonset(["first", "second"], "noun")
        self.assertEqual([p.lemma for p in from_string_list.paradigm], ["first", "second"])

        from_paradigm = oe_formset.read_canonset({ "lemma": "lem", "plural": "plur" }, "noun")
        self.assertEqual([from_paradigm.paradigm.lemma, from_paradigm.paradigm.plural], ["lem", "plur"])

        from_paradigm_list = oe_formset.read_canonset([{ "lemma": "first"}, { "lemma": "second" }], "noun")
        self.assertEqual([p.lemma for p in from_paradigm_list.paradigm], ["first", "second"])

        full_dict = oe_formset.read_canonset({ "form": "form", "dialect": "midlands"}, "noun")
        self.assertEqual([full_dict.paradigm.lemma, full_dict.dialect], ["form", "midlands"])

    def test_oe_paradigm(self):
        from_string = oe_formset.read_paradigm("form", "noun")
        self.assertEqual(from_string.lemma, "form")

        from_string_list = oe_formset.read_metaform(["first", "second"], "noun")
        self.assertEqual([p.lemma for p in from_string_list.paradigm], ["first", "second"])

        with_noun = oe_formset.read_paradigm({ "lemma": "lem", "oblique": "ob" }, "noun")
        self.assertEqual([with_noun.lemma, with_noun.oblique], ["lem", "ob"])

        with_default_oblique = oe_formset.read_paradigm({ "lemma": "lem" }, "noun")
        self.assertEqual([with_default_oblique.lemma, with_default_oblique.oblique], ["lem", "lem|e"])

        with_verb = oe_formset.read_paradigm({ "infinitive": "form|an", "past": "formod", "past-participle": "ġe-formod" }, "verb")
        self.assertEqual([with_verb.infinitive, with_verb.past, with_verb.past_participle], ["form|an", "formod", "ġe-formod"])

        dict_list = oe_formset.read_paradigm([{ "lemma": "first" }, { "lemma": "second" }], "noun")
        self.assertEqual([p.lemma for p in dict_list], ["first", "second"])

    def test_mne_paradigm(self):
        from_string = mne_formset.read_paradigm("form", "noun")
        self.assertEqual(from_string.lemma, "form")

        with_noun = mne_formset.read_paradigm({ "lemma": "sg", "plural": "pl" }, "noun")
        self.assertEqual([with_noun.lemma, with_noun.plural], ["sg", "pl"])

        with_default_plural = mne_formset.read_paradigm({ "lemma": "sg" }, "noun")
        self.assertEqual([with_default_plural.lemma, with_default_plural.plural], ["sg", "sgs"])

        with_adj = mne_formset.read_paradigm({ "lemma": "form", "comparative": "former", "superlative": "formest" }, "adj")
        self.assertEqual([with_adj.lemma, with_adj.comparative, with_adj.superlative], ["form", "former", "formest"])

        with_verb = mne_formset.read_paradigm({ "lemma": "form", "past": "formed", "past-participle": "formed" }, "verb")
        self.assertEqual([with_verb.lemma, with_verb.past, with_verb.past_participle], ["form", "formed", "formed"])

if __name__ == '__main__':    
    unittest.main()
