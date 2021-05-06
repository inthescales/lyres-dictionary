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
        self.assertForm(["ad", "arguere", "or"], "adargutor") #*
        
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
        self.assertForm(["ad", "bibere"], "abbibe")
        
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
        self.assertForm(["com", "quaerere", "or"], "conquisitor") #*
        self.assertForm(["com", "sequi", "nt"], "consequent")
        self.assertForm(["com", "tenere", "nt"], "continent")
        self.assertForm(["com", "venire", "ion"], "convention")
        
        # com -> co
        self.assertForm(["com", "arguere", "or"], "coargutor") #*
        self.assertForm(["com", "esse", "nt"], "coessent") #*
        self.assertForm(["com", "haerere", "nt"], "coherent")
        self.assertForm(["com", "ire", "ion"], "coition")
        self.assertForm(["com", "ordinare", "ion"], "coordination")
        
        #com -> co+
        self.assertForm(["com", "laborare", "or"], "collaborator")
        self.assertForm(["com", "regere", "ive"], "corrective")
        
        # 'dis' ----------
        
        self.assertForm(["dis", "apparere", "nt"], "disapparent") #*
        self.assertForm(["dis", "battuere", "nt"], "disbatant") #*
        self.assertForm(["dis", "cernere", "ion"], "discretion")
        self.assertForm(["dis", "aequus", "ity"], "disequity") #*
        self.assertForm(["dis", "gradi", "ion"], "digression")
        self.assertForm(["dis", "hortari"], "dishort")
        self.assertForm(["dis", "identa", "ity"], "disidentity") #*
        self.assertForm(["dis", "jacere"], "disject")
        self.assertForm(["dis", "mittere", "ion"], "dismission") #*
        self.assertForm(["dis", "numerare", "ion"], "disnumeration") #*
        self.assertForm(["dis", "pandere", "ion"], "dispansion") #*
        self.assertForm(["dis", "quaerere", "ion"], "disquisition")
        self.assertForm(["dis", "secare", "ion"], "dissection")
        self.assertForm(["dis", "trahere", "ion"], "distraction")
        self.assertForm(["dis", "unus", "ity"], "disunity")
        
        # dis -> di
        self.assertForm(["dis", "ducere", "ion"], "diduction") #*
        self.assertForm(["dis", "luere", "ion"], "dilution")
        self.assertForm(["dis", "regere", "ion"], "direction")
        self.assertForm(["dis", "vagari", "ion"], "divagation")
        
        # dis -> di+
        self.assertForm(["dis", "ferre", "nt"], "different")
        
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
        self.assertForm(["ex", "donare", "ion"], "edonation") #*
        self.assertForm(["com", "sequi", "nt"], "consequent")
        self.assertForm(["ex", "jacere", "ion"], "ejection")
        # self.assertForm(["ex", "ferre", "ion"], "elation") # BROKEN - this form doesn't work. Need estimate form when assimilating.
        self.assertForm(["ex", "mergere", "nt"], "emergent")
        self.assertForm(["ex", "numerare", "or"], "enumerator")
        self.assertForm(["ex", "regere", "ion"], "erection")
        self.assertForm(["ex", "vadere", "ive"], "evasive")
        self.assertForm(["ex", "numerare", "or"], "enumerator")
        
        # ex -> ex/
        self.assertForm(["ex", "sequi", "or"], "executor")
        
        # ex -> e+
        self.assertForm(["ex", "fluere", "nt"], "effluent")
        
        # 'in' ----------
        
        # in + a-, as in 'inactive'
        self.assertForm(["in", "ducere", "ion"], "induction")
        self.assertForm(["in", "clinare", "ion"], "inclination")
        self.assertForm(["in", "ducere", "ive"], "inductive")
        self.assertForm(["in", "educare", "ble"], "ineducable") #*
        self.assertForm(["in", "facere", "ion"], "infection")
        self.assertForm(["in", "gerere", "ion"], "ingestion")
        self.assertForm(["in", "habitare", "nt"], "inhabitant")
        self.assertForm(["in", "imitari", "ble"], "inimitable") #*
        self.assertForm(["in", "numerare", "ble"], "innumerable") #*
        self.assertForm(["in", "optare", "ive"], "inoptive") #*
        self.assertForm(["in", "quaerere", "ive"], "inquisitive")
        self.assertForm(["in", "scribere", "ion"], "inscription")
        self.assertForm(["in", "trudere", "ive"], "intrusive")

        # in -> im
        self.assertForm(["in", "bibere"], "imbibe")
        self.assertForm(["in", "mergere", "ion"], "immersion")
        self.assertForm(["in", "pellere", "ive"], "impulsive")
        self.assertForm(["in", "urbs", "ify"], "inurbify") #*
        self.assertForm(["in", "vadere", "ion"], "invasion")
        
        # in -> i+
        self.assertForm(["in", "ludere", "ion"], "illusion")
        self.assertForm(["in", "rogare", "nt"], "irrogant") #*
        

    # Miscellaneous tests confirming that real words have the correct forms.
    def testActualForms(self):        
        self.assertForm(["com", "venire", "ion"], "convention")
    
    # Helpers ==========
    
    def assertForm(self, keys, form):
        word = word_for_keys(keys, self.morphothec)
        self.assertEqual(composer.get_form(word), form)

if __name__ == '__main__':    
    unittest.main()