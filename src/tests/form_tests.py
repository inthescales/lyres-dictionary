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
        
        self.assertForm(["ad", "arguere", "or"], "adargutor") #*
        self.assertForm(["ad", "ducere", "ion"], "adduction")
        self.assertForm(["ad", "educare", "ion"], "adeducation") #*
        self.assertForm(["ad", "haerere", "ion"], "adhesion")
        self.assertForm(["ad", "jurare"], "adjure")
        self.assertForm(["ad", "mirari", "ion"], "admiration")
        self.assertForm(["ad", "optare", "ion"], "adoption")
        self.assertForm(["ad", "venire", "ure"], "adventure")
        
        # ad -> a
        self.assertForm(["ad", "scandere", "nt"], "ascendant")
        self.assertForm(["ad", "specere"], "aspect")
        self.assertForm(["ad", "stringere"], "astrict")
        
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
        self.assertForm(["dis", "aequa", "ity"], "disequity") #*
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
        self.assertForm(["sub", "bracchium", "al"], "subbrachial")
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
        
    def testLRDissimilation(self):        
        score = 0

        # Has an L, ends in L
        score += self.countForm(["familia", "al"], "familial")
        score += self.countForm(["labia", "al"], "labial")
        score += self.countForm(["lingua", "al"], "lingual")
        score += self.countForm(["littera", "al"], "literal")
        score += self.countForm(["locus", "al"], "local")
        score += self.countForm(["helix", "al"], "helical")
        score += self.countForm(["latus", "al"], "lateral")
        score += self.countForm(["lex", "al"], "legal")
        score += self.countForm(["limen", "al"], "liminal")
        score += self.countForm(["glacies", "al"], "glacial")
        
        # Has an L, ends in R
        score += self.countForm(["ala", "al"], "alar")
        score += self.countForm(["columna", "al"], "columnar")
        score += self.countForm(["familia", "al"], "familiar")
        score += self.countForm(["insula", "al"], "insular")
        score += self.countForm(["linea", "al"], "linear")
        score += self.countForm(["luna", "al"], "lunar")
        score += self.countForm(["stella", "al"], "stellar")
        score += self.countForm(["angulus", "al"], "angular")
        score += self.countForm(["anulus", "al"], "annular")
        score += self.countForm(["oculus", "al"], "ocular")
        score += self.countForm(["populus", "al"], "popular")
        score += self.countForm(["sol", "al"], "solar")
        
        self.assertTrue(score >= 15)
        
    def testStemChange(self):
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
        
        # Latin nouns, 1st declension
        self.assertForm(["anima", "al"], "animal")
        self.assertForm(["bestia", "al"], "bestial")
        self.assertForm(["littera", "al"], "literal")
        self.assertForm(["materia", "al"], "material")
        self.assertForm(["persona", "al"], "personal")
        self.assertForm(["ancilla", "ary"], "ancillary")
        self.assertForm(["culina", "ary"], "culinary")
        self.assertForm(["epistula", "ary"], "epistulary")
        self.assertForm(["littera", "ary"], "literary")
        self.assertForm(["pecunia", "ary"], "pecuniary")
        self.assertFormIn(["columba", "arium"], ["columbary", "columbarium"])
        self.assertFormIn(["planeta", "arium"], ["planetary", "planetarium"])
        self.assertFormIn(["terra", "arium"], ["terrary", "terrarium"])
        self.assertForm(["branchia", "ate-bodypart"], "branchiate")
        self.assertForm(["labia", "ate-bodypart"], "labiate")
        self.assertForm(["lingua", "ate-bodypart"], "linguate")
        self.assertForm(["mamma", "ate-bodypart"], "mammate")
        self.assertForm(["idea", "ate-secretion"], "ideate")
        self.assertForm(["urina", "ate-secretion"], "urinate")
        self.assertForm(["aquila", "ine"], "aquiline")
        self.assertForm(["columba", "ine"], "columbine")
        self.assertForm(["femina", "ine"], "feminine")
        self.assertForm(["rana", "ine"], "ranine")
        self.assertForm(["palma", "etum"], "palmetum")
        self.assertForm(["copia", "ous"], "copious")
        self.assertForm(["fabula", "ous"], "fabulous")
        self.assertForm(["fama", "ous"], "famous")
        self.assertForm(["gloria", "ous"], "glorious")
        self.assertForm(["pecunia", "ous"], "pecunious")
        self.assertForm(["aqua", "fer"], "aquifer")
        self.assertForm(["mamma", "fer"], "mammifer")
        self.assertForm(["arma", "ger"], "armiger")
        self.assertForm(["campana", "form"], "campaniform")
        self.assertForm(["columna", "form"], "columniform")
        self.assertForm(["luna", "form"], "luniform")
        self.assertForm(["palma", "form"], "palmiform")
        self.assertForm(["rana", "form"], "raniform")
        self.assertForm(["femina", "cide"], "feminicide")
        self.assertForm(["filia", "cide"], "filicide")
        self.assertForm(["gallina", "cide"], "gallinicide")
        self.assertForm(["herba", "cide"], "herbicide")
        
        # Latin nouns, 2nd declension
        self.assertForm(["astrum", "al"], "astral")
        self.assertForm(["bracchium", "al"], "brachial")
        self.assertForm(["carcer", "al"], "carceral")
        # self.assertForm(["fluvius", "al"], "fluvial")
        self.assertForm(["frater", "al"], "fraternal")
        self.assertForm(["populus", "al"], "popular")
        self.assertForm(["auxilium", "ary"], "auxiliary")
        self.assertForm(["capillus", "ary"], "capillary")
        self.assertForm(["exemplum", "ary"], "exemplary")
        self.assertForm(["numerus", "ary"], "numerary")
        self.assertForm(["auxilium", "ary"], "auxiliary")
        self.assertFormIn(["granus", "arium"], ["granarium", "granary"])
        self.assertFormIn(["liber", "arium"], ["librarium", "library"])
        self.assertForm(["auxilium", "ary"], "auxiliary")
        self.assertForm(["bracchium", "ate-bodypart"], "brachiate")
        self.assertForm(["capillus", "ate-bodypart"], "capillate")
        self.assertForm(["folium", "ate-bodypart"], "foliate")
        self.assertForm(["granus", "ate-bodypart"], "granate")
        self.assertForm(["oculus", "ate-bodypart"], "oculate")
        self.assertForm(["insectum", "ile"], "insectile")
        self.assertForm(["puer", "ile"], "puerile")
        self.assertForm(["servus", "ile"], "servile")
        self.assertForm(["vir", "ile"], "virile")
        self.assertForm(["asinus", "ine"], "asinine")
        self.assertForm(["equus", "ine"], "equine")
        self.assertForm(["labyrinthus", "ine"], "labyrinthine")
        self.assertForm(["serpentus", "ine"], "serpentine")
        self.assertForm(["corvus", "id-descendant"], "corvid")
        self.assertForm(["pinus", "etum"], "pinetum")
        self.assertForm(["servus", "tude"], "servitude")
        self.assertForm(["cancer", "ous"], "cancrous")
        self.assertForm(["ferrum", "ous-material"], "ferrous")
        self.assertForm(["numerus", "ous"], "numerous")
        self.assertForm(["officium", "ous"], "officious")
        self.assertForm(["rapax", "ous"], "rapacious")
        self.assertForm(["deus", "ify"], "deify")
        self.assertForm(["exemplum", "ify"], "exemplify")
        self.assertForm(["modus", "ify"], "modify")
        self.assertForm(["nullus", "ify"], "nullify")
        self.assertForm(["signum", "ify"], "signify")
        self.assertForm(["conus", "fer"], "conifer")
        self.assertForm(["scutum", "fer"], "scutifer")
        self.assertForm(["bellum", "ger", "nt"], "belligerent")
        self.assertForm(["cancer", "form"], "cancriform")
        self.assertForm(["cerebrum", "form"], "cerebriform")
        self.assertForm(["nasus", "form"], "nasiform")
        self.assertForm(["ovum", "form"], "oviform")
        self.assertForm(["insectum", "cide"], "insecticide")
        self.assertForm(["insectum", "cide"], "insecticide")
        self.assertForm(["vir", "cide"], "viricide")
        self.assertForm(["virus", "cide"], "viricide")

        # Latin nouns, 3nd declension
        self.assertForm(["caput", "al"], "capital")
        self.assertForm(["caro", "al"], "carnal")
        self.assertForm(["cordis", "al"], "cordial")
        self.assertForm(["hospes", "al"], "hospital")
        self.assertForm(["rex", "al"], "regal")
        self.assertForm(["imago", "ary"], "imaginary")
        self.assertForm(["lapis", "ary"], "lapidary")
        self.assertForm(["miles", "ary"], "military")
        self.assertForm(["pulmo", "ary"], "pulmonary")
        self.assertForm(["tempus", "ary"], "temporary")
        self.assertFormIn(["avis", "arium"], ["aviarium", "aviary"])
        self.assertFormIn(["apes", "arium"], ["apiarium", "apiary"])
        self.assertForm(["caput", "ate-bodypart"], "capitate")
        self.assertForm(["corpus", "ate-bodypart"], "corporate")
        self.assertForm(["dens", "ate-bodypart"], "dentate")
        self.assertForm(["pulmo", "ate-bodypart"], "pulmonate")
        self.assertForm(["radix", "ate-bodypart"], "radicate")
        self.assertForm(["lact", "ate-secretion"], "lactate")
        self.assertForm(["hostis", "ile"], "hostile")
        self.assertForm(["juvenis", "ile"], "juvenile")
        self.assertForm(["senex", "ile"], "senile")
        self.assertForm(["bos", "ine"], "bovine")
        self.assertForm(["felis", "ine"], "feline")
        self.assertForm(["leo", "ine"], "leonine")
        self.assertForm(["ovis", "ine"], "ovine")
        self.assertForm(["sphinx", "ine"], "sphingine")
        self.assertForm(["avis", "ian-animal"], "avian")
        self.assertForm(["canis", "id-descendant"], "canid")
        self.assertForm(["felis", "id-descendant"], "felid")
        self.assertForm(["homo", "id-descendant"], "hominid")
        self.assertForm(["arbor", "esce-plant", "nt"], "arborescent")
        self.assertForm(["ex", "flos", "esce-plant"], "effloresce")
        self.assertForm(["frons", "esce-plant"], "frondesce")
        self.assertForm(["apes", "culture"], "apiculture")
        self.assertForm(["avis", "culture"], "aviculture")
        self.assertForm(["bos", "culture"], "boviculture")
        self.assertForm(["mare", "culture"], "mariculture")
        self.assertForm(["vermis", "culture"], "vermiculture")
        self.assertForm(["arbor", "ous"], "arborous")
        self.assertForm(["caro", "ous"], "carnous")
        self.assertForm(["carbo", "ous"], "carbonous")
        self.assertForm(["febris", "ous"], "febrous")
        self.assertForm(["gramen", "ous"], "graminous")
        self.assertForm(["carbo", "ify"], "carbonify")
        self.assertForm(["crux", "ify"], "crucify")
        self.assertForm(["lapis", "ify"], "lapidify")
        self.assertForm(["mors", "ify"], "mortify")
        self.assertForm(["pax", "ify"], "pacify")
        self.assertForm(["crux", "fer"], "crucifer")
        self.assertForm(["lux", "fer"], "lucifer")
        self.assertForm(["proles", "fer", "ate"], "proliferate")
        self.assertForm(["thuris", "fer"], "thurifer")
        self.assertForm(["clavis", "ger"], "claviger")
        self.assertForm(["calix", "form"], "caliciform")
        self.assertForm(["caseus", "form"], "caseiform")
        self.assertForm(["falx", "form"], "falciform")
        self.assertForm(["funis", "form"], "funiform")
        self.assertForm(["homo", "form"], "hominiform")
        self.assertForm(["grex", "cide"], "gregicide")
        self.assertForm(["pater", "cide"], "patricide")
        self.assertForm(["senex", "cide"], "senicide")
        self.assertForm(["soror", "cide"], "sororicide")
        self.assertForm(["vitis", "cide"], "viticide")
        
        # Latin nouns, 4th declension
        self.assertForm(["casus", "al"], "casual")
        self.assertForm(["manus", "al"], "manual")
        self.assertFormIn(["os-remains", "arium"], ["ossuarium", "ossuary"])
        self.assertForm(["cornus", "ate-bodypart"], "cornuate")
        self.assertForm(["lacus", "ine"], "lacustrine")
        self.assertForm(["quercus", "ine"], "quercine")
        self.assertForm(["fructus", "ous"], "fructuous")
        self.assertForm(["lacus", "ine"], "lacustrine")
        self.assertForm(["manus", "form"], "maniform")

        # Latin nouns, 5th declension
        self.assertForm(["facies", "al"], "facial")
        self.assertForm(["dies", "ary"], "diary")
        self.assertForm(["facies", "al"], "facial")
        
        # Latin nouns, indeclinable
        self.assertForm(["unus", "ity"], "unity")
        self.assertForm(["duo", "al"], "dual")
        self.assertForm(["ad", "nihil", "ate"], "annihilate")
        
        # Latin adjectives, 1st/2nd declension
        self.assertForm(["acerba", "ity"], "acerbity")
        self.assertForm(["digna", "ity"], "dignity")
        self.assertForm(["aequa", "ity"], "equity")
        self.assertForm(["obscura", "ity"], "obscurity")
        self.assertForm(["tranquilla", "ity"], "tranquility")
        self.assertForm(["alta", "tude"], "altitude")
        self.assertForm(["certa", "tude"], "certitude")
        self.assertForm(["crassa", "tude"], "crassitude")
        self.assertForm(["pulchra", "tude"], "pulchritude")
        self.assertForm(["sola", "tude"], "solitude")
        self.assertForm(["digna", "ify"], "dignify")
        self.assertForm(["falsa", "ify"], "falsify")
        self.assertForm(["magna", "ify"], "magnify")
        self.assertForm(["puter", "ify"], "putrify")
        self.assertForm(["aequa", "ate"], "equate")
        self.assertForm(["integra", "ate"], "integrate")
        self.assertForm(["libera", "ate"], "liberate")
        self.assertForm(["valida", "ate"], "validate")
        self.assertForm(["stulta", "ify"], "stultify")
        self.assertForm(["maxima", "ize"], "maximize")
        self.assertForm(["minima", "ize"], "minimize")
        self.assertForm(["pessima", "ize"], "pessimize")
        self.assertForm(["privata", "ize"], "privatize")
        self.assertForm(["tranquilla", "ize"], "tranquilize")
        self.assertForm(["re", "cruda", "esce"], "recrudesce")
        self.assertForm(["matura", "esce"], "maturesce")
        self.assertForm(["puter", "esce", "nt"], "putrescent")
        self.assertFormIn(["antiqua", "arium"], ["antiquarium", "antiquary"])
        
        # Latin adjectives, 3rd declension
        self.assertForm(["communis", "ity"], "community")
        self.assertForm(["levis", "ity"], "levity")
        self.assertForm(["maior", "ity"], "majority")
        self.assertForm(["real", "ity"], "reality")
        self.assertForm(["stabilis", "ity"], "stability")
        self.assertForm(["humilis", "tude"], "humilitude")
        self.assertForm(["lenis", "tude"], "lenitude")
        self.assertForm(["similis", "tude"], "similitude")
        self.assertForm(["turpis", "tude"], "turpitude")
        self.assertForm(["mollis", "ify"], "mollify")
        self.assertForm(["debilis", "ate"], "debilitate")
        self.assertForm(["facilis", "ate"], "facilitate")
        self.assertForm(["levis", "ate"], "levitate")
        self.assertForm(["facilis", "ate"], "facilitate")
        
        # Latin verbs, 1st conjugation, suffixes
        self.assertForm(["curare", "ble"], "curable")
        self.assertForm(["damnare", "ble"], "damnable")
        self.assertForm(["delectare", "ble"], "delectable")
        self.assertForm(["laudare", "ble"], "laudable")
        self.assertForm(["tolerare", "ble"], "tolerable")
        self.assertForm(["fricare", "ile-verb"], "frictile")
        self.assertForm(["natare", "ile-verb"], "natatile")
        self.assertForm(["plicare", "ile-verb"], "plicatile")
        self.assertForm(["secare", "ile-verb"], "sectile")
        self.assertForm(["vibrare", "ile-verb"], "vibratile")
        self.assertForm(["fricare", "ion"], "friction")
        self.assertForm(["jubilare", "ion"], "jubilation")
        self.assertForm(["optare", "ion"], "option")
        self.assertForm(["secare", "ion"], "section")
        self.assertForm(["vibrare", "ion"], "vibration")
        self.assertForm(["generare", "ive"], "generative")
        self.assertForm(["laxare", "ive"], "laxative")
        self.assertForm(["laudare", "ive"], "laudative")
        self.assertForm(["narrare", "ive"], "narrative")
        self.assertForm(["stare", "ive"], "stative")
        self.assertForm(["curare", "or"], "curator")
        self.assertForm(["educare", "or"], "educator")
        self.assertForm(["liberare", "or"], "liberator")
        self.assertForm(["narrare", "or"], "narrator")
        self.assertForm(["praedari", "or"], "predator")
        self.assertForm(["abundare", "nt"], "abundant")
        self.assertForm(["errare", "nt"], "errant")
        self.assertForm(["fragrare", "nt"], "fragrant")
        self.assertForm(["migrare", "nt"], "migrant")
        self.assertForm(["militare", "nt"], "militant")
        
        # Latin verbs, 2nd conjugation, suffixes
        self.assertForm(["ardere", "nt"], "ardent")
        self.assertForm(["lucere", "nt"], "lucent")
        self.assertForm(["paenitere", "nt"], "penitent")
        self.assertForm(["torrere", "nt"], "torrent")
        self.assertForm(["valere", "nt"], "valent")
        self.assertForm(["delere", "ble"], "delible")
        self.assertForm(["horrere", "ble"], "horrible")
        self.assertForm(["delere", "ion"], "deletion")
        self.assertForm(["manere", "ion"], "mansion")
        self.assertForm(["movere", "ion"], "motion")
        self.assertForm(["sedere", "ion"], "session")
        self.assertForm(["tueri", "ion"], "tuition")

        # Latin verbs, 3rd conjugation, suffixes
        self.assertForm(["crescere", "nt"], "crescent")
        self.assertForm(["currere", "nt"], "current")
        self.assertForm(["docere", "nt"], "docent")
        self.assertForm(["gradi", "nt"], "gradient")
        self.assertForm(["nasci", "nt"], "nascent")
        self.assertForm(["credere", "ble"], "credible")
        self.assertForm(["fallere", "ble"], "fallible")
        self.assertForm(["fungi", "ble"], "fungible")
        self.assertForm(["tangere", "ble"], "tangible")
        self.assertForm(["vincere", "ble"], "vincible")
        self.assertForm(["figere", "ion"], "fixation")
        self.assertForm(["fungi", "ion"], "function")
        self.assertForm(["mittere", "ion"], "mission")
        self.assertForm(["petere", "ion"], "petition")
        self.assertForm(["scandere", "ion"], "scansion")

        # Latin verbs, 4th conjugation, suffixes
        self.assertForm(["nutrire", "nt"], "nutrient")
        self.assertForm(["mugire", "nt"], "mugient")
        self.assertForm(["oriri", "nt"], "orient")
        self.assertForm(["salire", "nt"], "salient")
        self.assertForm(["sentire", "nt"], "sentient")
        self.assertForm(["audire", "ble"], "audible")
        self.assertForm(["audire", "ion"], "audition")
        self.assertForm(["ex", "haurire", "ion"], "exhaustion")
        self.assertForm(["partiri", "ion"], "partition")
        self.assertFormIn(["salire", "ion"], ["saltion", "salition"])
        self.assertForm(["aperire", "ure"], "aperture")
        self.assertForm(["venire", "ure"], "venture")
        self.assertForm(["in", "vestire", "ure"], "investiture")

        # preposition + verb
        self.assertForm(["com", "coquere"], "concoct")
        self.assertForm(["com", "fateri"], "confess")
        self.assertForm(["com", "finire"], "confine")
        self.assertForm(["com", "venire"], "convene")
        self.assertForm(["ab", "battuere"], "abate")
        self.assertForm(["ad", "facere"], "affect")
        self.assertForm(["dis", "apparere"], "disappear")
        self.assertForm(["dis", "cernere"], "discern")
        self.assertForm(["ex", "facere"], "effect")
        self.assertForm(["in", "bibere"], "imbibe")
        self.assertForm(["re", "agere"], "react")
        self.assertForm(["re", "apparere"], "reappear")
        self.assertForm(["per", "facere"], "perfect")
        
        # preposition + verb + suffix
        self.assertForm(["ad", "figere", "ion"], "affixation")
        self.assertForm(["com", "battuere", "nt"], "combatant")
        self.assertForm(["com", "fateri", "ion"], "confession")
        self.assertForm(["com", "venire", "ion"], "convention")
        self.assertForm(["de", "caedere", "ion"], "decision")
        self.assertForm(["ex", "citare", "ion"], "excitation")
        self.assertForm(["ex", "facere", "nt"], "efficient")
        self.assertForm(["ex", "facere", "ive"], "effective")
        self.assertForm(["in", "cantare", "ion"], "incantation")
        self.assertForm(["in", "capere", "nt"], "incipient")
        self.assertForm(["ob", "cadere", "ion"], "occasion")
        self.assertForm(["re", "agere", "ion"], "reaction")
        self.assertForm(["re", "capere", "ive"], "receptive")
        self.assertForm(["re", "currere", "nt"], "recurrent")
        self.assertForm(["per", "emere", "ory"], "peremptory")
        
        # prefix + verb
        self.assertForm(["re-again", "cruda", "esce"], "recrudesce")
        
        # two suffixes
        self.assertForm(["com", "fidere", "nce", "al"], "confidential")
        self.assertForm(["diversa", "ify", "ion"], "diversification")
        self.assertForm(["duo", "al", "ity"], "duality")
        self.assertForm(["esse", "nce", "al"], "essential")
        self.assertForm(["funis", "pote-power", "nt"], "funipotent")
        
        # relative constructions
        self.assertForm(["ad", "glomus", "ate"], "agglomerate")
        self.assertForm(["ad", "grex", "ate"], "aggregate")
        self.assertForm(["ad", "nihil", "ate"], "annihilate")
        self.assertForm(["com", "grex", "ate"], "congregate")
        self.assertForm(["com", "mensa", "al"], "commensal")
        self.assertForm(["com", "mensus", "ate"], "commensurate")
        self.assertForm(["de", "fenestra", "ate"], "defenestrate")
        self.assertForm(["ex", "onus", "ate"], "exonerate")
        self.assertForm(["ex", "pectus", "ate"], "expectorate")
        self.assertForm(["ex", "radix", "ate"], "eradicate")
        self.assertForm(["in", "carcer", "ate"], "incarcerate")
        self.assertForm(["in", "corpus", "ate"], "incorporate")
        self.assertForm(["in", "persona", "ate"], "impersonate")
        self.assertForm(["in", "semen", "ate"], "inseminate")
        self.assertForm(["re-again", "in", "caro", "ate", "ion"], "reincarnation")
        self.assertForm(["inter", "columna", "al"], "intercolumnar")
        self.assertForm(["inter", "crus", "al"], "intercrural")
        self.assertForm(["inter", "dens", "al"], "interdental")
        self.assertForm(["inter", "planeta", "ary"], "interplanetary")
        self.assertForm(["inter", "stella", "al"], "interstellar")
        self.assertForm(["praeter", "natura", "al"], "preternatural")
        self.assertForm(["pre", "industria", "al"], "preindustrial")
        self.assertForm(["sub", "apex", "al"], "subapical")
        self.assertForm(["sub", "bracchium", "al"], "subbrachial")
        self.assertForm(["sub", "limen", "al"], "subliminal")
        self.assertForm(["super", "natura", "al"], "supernatural")
        self.assertForm(["trans", "dermis", "al"], "transdermal")
        self.assertForm(["trans", "luna", "al"], "translunar")
        
        # numerical constructions
        self.assertForm(["two-join", "camera", "al"], "bicameral")
        self.assertForm(["two-join", "latus", "al"], "bilateral")
        self.assertForm(["three-join", "geminus", "al"], "trigeminal")
        self.assertForm(["three-join", "angulus", "al"], "triangular")
        self.assertForm(["three-join", "latus", "al"], "trilateral")
        self.assertForm(["four-join", "latus", "al"], "quadrilateral")
    
    # Tests confirming that exception cases work as expected.
    def testFormException(self):
        # Latin nouns
        # aerial
        self.assertForm(["aqua", "ous"], "aqueous")
        self.assertForm(["arbor", "al"], "arboreal")
        self.assertForm(["homo", "cide"], "homicide")
        self.assertForm(["fructus", "esce-plant", "nt"], "fructescent") 
        self.assertForm(["homo", "cide"], "homicide")
        self.assertForm(["lapis", "ous"], "lapideous")
        self.assertForm(["lignum", "ous"], "ligneous")
        self.assertForm(["manus", "form"], "maniform")
        self.assertForm(["nux", "ous"], "nuceous")
        self.assertForm(["vitis", "etum"], "viticetum")
        
        # Latin verbs
        self.assertForm(["debere", "or"], "debtor")
        self.assertForm(["jurare", "or"], "juror")
        
        # Verbs with alternate prefixed fors
        self.assertFormIn(["cadere", "nce"], ["cadence", "cadency"])
        self.assertForm(["in", "cadere", "nt"], "incident")
        self.assertForm(["capere", "ive"], "captive")
        self.assertForm(["re", "capere", "ive"], "receptive")
        self.assertForm(["re", "capere", "nt"], "recipient")
        self.assertForm(["damnare", "ion"], "damnation")
        self.assertForm(["com", "damnare", "ion"], "condemnation")
        self.assertForm(["facere", "ion"], "faction")
        self.assertForm(["in", "facere", "ion"], "infection")
        self.assertForm(["ex", "facere", "nt"], "efficient")
        self.assertForm(["in", "habere", "ion"], "inhibition")
        self.assertForm(["ad", "jacere", "nt"], "adjacent")
        self.assertForm(["com", "jacere", "ure"], "conjecture")
        self.assertForm(["re", "jacere"], "reject")
        self.assertForm(["salire", "nt"], "salient")
        self.assertForm(["re", "salire", "nt"], "resilient")
        self.assertForm(["scandere", "ion"], "scansion")
        self.assertForm(["ad", "scandere", "ion"], "ascension")
        self.assertForm(["ad", "scandere", "nt"], "ascendant")
        self.assertForm(["tenere", "ion"], "tension")
        self.assertForm(["ad", "tenere", "ion"], "attention")
        self.assertForm(["tenere", "nt"], "tenent")
        self.assertForm(["com", "tenere", "nt"], "continent")
        self.assertForm(["violare", "nt"], "violent")
        
        # Verbs with exceptions for "ble"
        self.assertForm(["pre", "dicere", "ble"], "predictable")
        self.assertForm(["trans", "ferre", "ble"], "transferable")
        self.assertForm(["flectere", "ble"], "flexible")
        #self.assertForm(["sub", "mergere", "ble"], "submersible")
        self.assertForm(["ad", "mittere", "ble"], "admissible")
        self.assertForm(["movere", "ble"], "movable")
        self.assertForm(["com", "plere", "ble"], "completable")
        self.assertForm(["com", "prehendere", "ble"], "comprehensible")
        self.assertForm(["ad", "quaerere", "ble"], "acquirable")
        self.assertForm(["re", "vertere", "ble"], "reversible")
        self.assertForm(["videre", "ble"], "visible")
    
    # Tests that forms that were made impossible in order to make other forms possible still don't work.
    # If these fail, it may not be a problem, but I should confirm that no other desired forms were lost.
    def testUnrealizedForms(self):
        self.assertFormNot(["humilis", "ate"], "humiliate")
        
        self.assertFormNot(["de", "cadere", "nt"], "decadent")
        self.assertFormNot(["ex", "sanguis", "ate"], "exsanguinate")
    
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
        
    def countForm(self, keys, form):
        word = word_for_keys(keys, self.morphothec)
        composed = composer.get_form(word)
        if composed == form:
            return 1
        else:
            return 0

if __name__ == '__main__':    
    unittest.main()