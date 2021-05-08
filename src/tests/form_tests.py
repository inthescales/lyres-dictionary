import unittest

from src.morphothec import Morphothec
from src.generator import word_for_keys
import src.composer as composer

class FormTests(unittest.TestCase):
    def setUp(self):
        self.morphothec = Morphothec(["data/morphs-latin.json", "data/morphs-greek.json"])

    # Tests that prefix sound assimilation resolves correctly.
    def testPrefixAssimilation(self):
        
        # 'ab' ----------
        self.assertForm(["ab", "ambulare", "ion"], "abambulation") #*
        self.assertForm(["ab", "ducere", "ion"], "abduction")
        self.assertForm(["ab", "errare", "ion"], "aberration")
        self.assertForm(["ab", "grex", "ate"], "abgregate")
        self.assertForm(["ab", "horrere"], "abhor")
        self.assertForm(["ab", "ire", "nt"], "abient")
        self.assertForm(["ab", "jacere", "ion"], "abjection")
        self.assertForm(["ab", "lact", "ate"], "ablactate")
        self.assertForm(["ab", "negare", "ion"], "abnegation")
        self.assertForm(["ab", "oriri", "ion"], "abortion")
        self.assertForm(["ab", "rogare", "ion"], "abrogation")
        self.assertForm(["ab", "solvere", "ion"], "absolution")
        self.assertForm(["ab", "uti"], "abuse")
        
        # ab -> a
        self.assertForm(["ab", "movere"], "amove")
        self.assertForm(["ab", "pellere", "ion"], "apulsion") #*
        self.assertForm(["ab", "vertere", "ion"], "aversion")
        
        # ab -> abs
        self.assertForm(["ab", "condere"], "abscond")
        self.assertForm(["ab", "quaerere", "ion"], "absquisition") #*
        self.assertForm(["ab", "trahere", "ion"], "abstraction")
        
        # ab -> au
        self.assertForm(["ab", "ferre", "nt"], "auferent") #*
        
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
        
        self.assertForm(["com", "battuere"], "combate") #*
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
        
        # 'ob' ----------

        self.assertForm(["ob", "ambulare"], "obambulate")
        self.assertForm(["ob", "battuere", "nt"], "obbatant") #*
        self.assertForm(["ob", "durare", "ion"], "obduration")
        self.assertForm(["ob", "errare", "ion"], "oberration")
        self.assertForm(["ob", "gerere", "ion"], "obgestion") #*
        self.assertForm(["ob", "haurire", "ion"], "obhaustion") #*
        self.assertForm(["ob", "ignorare", "nt"], "obignorant") #*
        self.assertForm(["ob", "jacere", "ion"], "objection")
        self.assertForm(["ob", "ligare", "ion"], "obligation")
        self.assertForm(["ob", "nectare", "ion"], "obnection")
        self.assertForm(["ob", "ordinare", "ure"], "obordinature") #*
        self.assertForm(["ob", "quaerere", "or"], "obquisitor") #*
        self.assertForm(["ob", "rumpere", "nt"], "obrumpent")
        self.assertForm(["ob", "sequi", "nt"], "obsequent")
        self.assertForm(["ob", "temperare"], "obtemper")
        self.assertForm(["ob", "volare"], "obvolate")
        
        # ob -> o
        # Before 'st', as in ostentatious
        self.assertForm(["ob", "mittere", "ion"], "omission")
        
        # ob -> o+
        self.assertForm(["ob", "cadere", "ion"], "occasion")
        self.assertForm(["ob", "ferre"], "offer")
        self.assertForm(["ob", "premere", "ion"], "oppression")
        
        # 'se' ----------
        # b
        self.assertForm(["se", "cedere", "ion"], "secession")
        self.assertForm(["se", "ducere", "ion"], "seduction")
        self.assertForm(["se", "ferre", "nt"], "seferent") #*
        self.assertForm(["se", "grex", "ate"], "segregate")
        self.assertForm(["se", "haerere", "ion"], "sehesion") #*
        self.assertForm(["se", "jungere", "ion"], "sejunction") #*
        self.assertForm(["se", "ligere", "ion"], "selection")
        self.assertForm(["se", "haerere", "ion"], "sehesion") #*
        self.assertForm(["se", "movere", "ion"], "semotion") #*
        self.assertForm(["se", "narrare", "or"], "senarrator") #*
        self.assertForm(["se", "parare", "ion"], "separation")
        self.assertForm(["se", "quaerere", "ion"], "sequisition") #*
        self.assertForm(["se", "quaerere", "ion"], "sequisition") #*
        self.assertForm(["se", "radere", "ive"], "serasive") #*
        self.assertForm(["se", "salire", "nt"], "sesilient") #*
        self.assertForm(["se", "trahere", "ion"], "setraction") #*
        self.assertForm(["se", "vocare", "ion"], "sevocation")
        
        # se -> sed
        self.assertForm(["se", "agere", "ion"], "sedaction") #*
        self.assertForm(["se", "errare", "nt"], "sederrant") #*
        self.assertForm(["se", "ire", "ion"], "sedition")
        self.assertForm(["se", "uti"], "seduse") #*
        
        # 'sub' ----------
        self.assertForm(["sub", "alternare"], "subalternate")
        self.assertForm(["sub", "bracchium", "al"], "subbracchial")
        self.assertForm(["sub", "ducere", "ion"], "subduction")
        self.assertForm(["sub", "errare", "ion"], "suberration")
        self.assertForm(["sub", "haurire", "ion"], "subhaustion") #*
        self.assertForm(["sub", "ire"], "subit") #*
        self.assertForm(["sub", "jacere", "nt"], "subjacent")
        self.assertForm(["sub", "linere", "ion"], "sublition")
        self.assertForm(["sub", "nasci", "nt"], "subnascent")
        self.assertForm(["sub", "oculus", "al"], "subocular")
        self.assertForm(["sub", "quaerere", "ive"], "subquisitive") #*
        self.assertForm(["sub", "secare"], "subsect")
        self.assertForm(["sub", "tendere"], "subtend")
        self.assertForm(["sub", "urbs", "al"], "suburbal") #*
        self.assertForm(["sub", "venire", "ion"], "subvention")
        
        # sub -> su+
        self.assertForm(["sub", "cedere", "ion"], "succession")
        self.assertForm(["sub", "ferre"], "suffer")
        self.assertForm(["sub", "gerere", "ion"], "suggestion")
        self.assertForm(["sub", "mandare"], "summand")
        self.assertForm(["sub", "ponere", "ion"], "supposition")
        self.assertForm(["sub", "rogare"], "surrogate")
        
        # sub -> sus
        
    def testStemChange(self):
        self.assertForm(["mugire", "nt"], "mugient")
        self.assertForm(["mugire", "nt"], "mugient")
        self.assertForm(["nutrire", "nt"], "nutrient")
        self.assertForm(["oriri", "nt"], "orient")
        self.assertForm(["sentire", "nt"], "sentient")
        self.assertForm(["com", "venire", "nt"], "convenient")
        self.assertForm(["re", "salire", "nt"], "resilient")
        
        self.assertFormIn(["experiri", "nce"], ["experience", "experiency"])
        self.assertFormIn(["scire", "nce"], ["science", "sciency"])
    
    def testStemRaise(self):
        self.assertForm(["credere", "ble"], "credible")
        self.assertForm(["fallere", "ble"], "fallible")
        self.assertForm(["fungi", "ble"], "fungible")
        self.assertForm(["legere", "ble"], "legible")
        self.assertForm(["neglegere", "ble"], "negligible")
        self.assertForm(["tangere", "ble"], "tangible")
        self.assertForm(["re", "vertere", "ble"], "reversible")
        self.assertForm(["in", "vincere", "ble"], "invincible")

    # Miscellaneous tests confirming that real words have the correct forms.
    def testActualForms(self):
        
        # noun + suffix
        self.assertForm(["amor", "ous"], "amorous")
        
        # preposition + verb
        self.assertForm(["com", "venire"], "convene")
        self.assertForm(["ab", "battuere"], "abate")
        self.assertForm(["dis", "apparere"], "disappear")
        self.assertForm(["in", "bibere"], "imbibe")
        self.assertForm(["re", "agere"], "react")
        self.assertForm(["re", "apparere"], "reappear")
        
        # verb + suffix
        self.assertForm(["abundare", "nt"], "abundant")
        self.assertForm(["adjutare", "nt-noun"], "adjutant")
        self.assertForm(["agere", "or"], "actor")
        self.assertForm(["alternare", "or"], "alternator")
        self.assertFormIn(["ambulare", "nce"], ["ambulance", "ambulancy"])
        self.assertForm(["apparere", "nt"], "apparent")
        self.assertForm(["appellare", "ion"], "appellation")
        self.assertForm(["ardere", "nt"], "ardent")
        self.assertForm(["attendere", "ion"], "attention")
        self.assertForm(["audire", "or"], "auditor")
        
        # preposition + verb + suffix
        self.assertForm(["com", "battuere", "nt"], "combatant")
        self.assertForm(["com", "venire", "ion"], "convention")
        self.assertForm(["de", "cadere", "nt"], "decident") #*
        self.assertForm(["ob", "cadere", "ion"], "occasion")
        self.assertForm(["re", "agere", "ion"], "reaction")
    
    # Miscellaneous tests confirming that real words have the correct forms.
    def testFormException(self):
        self.assertFormIn(["cadere", "nce"], ["cadence", "cadency"])
        self.assertForm(["in", "cadere", "nt"], "incident")
        self.assertForm(["com-intensive", "in", "cadere", "nt"], "coincident")
        self.assertFormNot(["de", "cadere", "nt"], "decadent")
    
    # Helpers ==========
    
    def assertForm(self, keys, form):
        word = word_for_keys(keys, self.morphothec)
        composed = composer.get_form(word)
        self.assertEqual(composed, form)

    def assertFormIn(self, keys, forms):
        word = word_for_keys(keys, self.morphothec)
        form = composer.get_form(word)
        self.assertIn(form, forms)
        
    def assertFormNot(self, keys, form):
        word = word_for_keys(keys, self.morphothec)
        composed = composer.get_form(word)
        self.assertNotEqual(composed, form)

if __name__ == '__main__':    
    unittest.main()