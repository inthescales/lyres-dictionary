import unittest

from src.morphothec import Morphothec
from src.generator import word_for_keys
import src.composer as composer

class FormTests(unittest.TestCase):
    def setUp(self):
        self.morphothec = Morphothec(["data/morphs-latin.json", "data/morphs-greek.json"])

    # Tests that prefix sound assimilation resolves correctly.
    def testPrefixAssimilation(self):
        
        # 'ad' ----------
        
        self.assertForm(["ad", "ducere", "ion"], "adduction")
        self.assertForm(["ad", "educare", "ion"], "adeducation") #*
        self.assertForm(["ad", "haerere", "ion"], "adhesion")
        self.assertForm(["ad", "jurare"], "adjure")
        self.assertForm(["ad", "mirari", "ion"], "admiration")
        self.assertForm(["ad", "optare", "ion"], "adoption")
        self.assertForm(["ad", "venire", "ure"], "adventure")
        
        # ad -> a
        # As in 'adapt'
        
        # ad doubling
        self.assertForm(["ad", "cedere", "ion"], "accession")
        self.assertForm(["ad", "figere", "ion"], "affixation")
        self.assertForm(["ad", "gradi", "ive"], "aggressive")
        self.assertForm(["ad", "ludere", "ion"], "allusion")
        self.assertForm(["ad", "nuntiare", "ion"], "annunciation")
        self.assertForm(["ad", "parere", "nt"], "apparent")
        self.assertForm(["ad", "rogare", "nt"], "arrogant")
        self.assertForm(["ad", "serere", "ion"], "assertion")
        
        # ad -> ac
        self.assertForm(["ad", "quaerere", "ion"], "acquisition")
        
        # ad -> ab
        # As in 'abbreviate'
        
        # 'com' ----------
        
        # com + b, as in 'combine' or 'combat'        
        self.assertForm(["com", "mandare"], "command")
        self.assertForm(["com", "pungere", "ion"], "compunction")
        
        # com -> con
        self.assertForm(["com", "cedere", "ion"], "concession")
        self.assertForm(["com", "ducere", "or"], "conductor")
        self.assertForm(["com", "fundere", "ion"], "confusion")
        self.assertForm(["com", "gerere", "ion"], "congestion")
        self.assertForm(["com", "nectare", "ive"], "connective")
        # con + q, as in 'conquest'
        self.assertForm(["com", "sequi", "nt"], "consequent")
        self.assertForm(["com", "tenere", "nt"], "continent")
        
        
        # com -> co
        # a, as in coagulate
        # e, as in coexist
        self.assertForm(["com", "haerere", "nt"], "coherent")
        self.assertForm(["com", "ire", "ion"], "coition")
        self.assertForm(["com", "ordinare", "ion"], "coordination")
        
        #com -> co+
        self.assertForm(["com", "laborare", "or"], "collaborator")
        self.assertForm(["com", "regere", "ive"], "corrective")
        
        # 'ex' ----------

        self.assertForm(["ex", "agere"], "exact")
        self.assertForm(["ex", "emere", "ion"], "exemption")
        self.assertForm(["ex", "haurire", "ion"], "exhaustion")
        self.assertForm(["ex", "ire"], "exit")
        self.assertForm(["ex", "onus", "ate"], "exonerate")
        self.assertForm(["ex", "pellere", "ion"], "expulsion")
        self.assertForm(["ex", "quaerere", "ion"], "exquisition")
        self.assertForm(["ex", "tendere", "ion"], "extension")
        
        # ex -> e
        # ebullient
        self.assertForm(["ex", "pellere", "ion"], "expulsion")
        # ex + d-, as in education
        self.assertForm(["ex", "jacere", "ion"], "ejection")
        # self.assertForm(["ex", "ferre", "ion"], "elation") # BROKEN - this form doesn't work. Need estimate form when assimilating.
        self.assertForm(["ex", "mergere", "nt"], "emergent")
        self.assertForm(["ex", "numerare", "or"], "enumerator")
        self.assertForm(["ex", "regere", "ion"], "erection")
        self.assertForm(["ex", "vadere", "ive"], "evasive")
        self.assertForm(["ex", "numerare", "or"], "enumerator")
        self.assertForm(["ex", "numerare", "or"], "enumerator")
        
        # ex -> ex/
        self.assertForm(["ex", "sequi", "or"], "executor")
        # ex + x-
        
        # ex -> e+
        self.assertForm(["ex", "fluere", "nt"], "effluent")
        
        # 'in' ----------
        
        # in + a-, as in 'inactive'
        self.assertForm(["in", "ducere", "ion"], "induction")
        self.assertForm(["in", "clinare", "ion"], "inclination")
        self.assertForm(["in", "ducere", "ive"], "inductive")
        # in + e-, as in 'inestimable'
        self.assertForm(["in", "facere", "ion"], "infection")
        self.assertForm(["in", "gerere", "ion"], "ingestion")
        self.assertForm(["in", "habitare", "nt"], "inhabitant")
        # in + i-, as in 'inimitable'
        # in + n-, as in 'innumerable'
        # in + o-, as in 'inoperative'
        self.assertForm(["in", "quaerere", "ive"], "inquisitive")
        self.assertForm(["in", "scribere", "ion"], "inscription")
        self.assertForm(["in", "trudere", "ive"], "intrusive")

        # in -> im
        self.assertForm(["in", "bibere"], "imbibe")
        self.assertForm(["in", "mergere", "ion"], "immersion")
        self.assertForm(["in", "pellere", "ive"], "impulsive")
        # in + u, can't think of an example
        
        # in -> i+
        self.assertForm(["in", "ludere", "ion"], "illusion")
        # in + r- as in 'irregular'
        


    # Miscellaneous tests confirming that real words have the correct forms.
    def testActualForms(self):        
        self.assertForm(["com", "venire", "ion"], "convention")
    
    # Helpers ==========
    
    def assertForm(self, keys, form):
        word = word_for_keys(keys, self.morphothec)
        self.assertEqual(composer.get_form(word), form)

if __name__ == '__main__':    
    unittest.main()