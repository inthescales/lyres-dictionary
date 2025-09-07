import src.language.modern_english.morphology as mne_morphology

from src.utils.logging import Logger

# Structures ===========================

class Paradigm_MnE_N():
	def __init__(self, singular, plural):
		self.singular = singular
		self.plural = plural

		self.lemma = self.singular

	def __str__(self):
		return "lemma: " + self.lemma + ", plural: " + self.plural

class Paradigm_MnE_A():
	def __init__(self, lemma, comparative, superlative):
		self.lemma = lemma
		self.comparative = comparative
		self.superlative = superlative

	def __str__(self):
		return "lemma: " + self.lemma + ", comparative: " + self.comparative + ", superlative: " + self.superlative

class Paradigm_MnE_V():
	def __init__(self, lemma, past, past_participle):
		self.lemma = lemma
		self.past = past
		self.past_participle = past_participle

	def __str__(self):
		return "lemma: " + self.lemma + ", past: " + str(self.past) + ", past-participle: " + str(self.past_participle)

# Parsing ============================

# Parse a paradigm from any valid input type
def read_paradigm(value, morph_type):
	if type(value) == dict:
		# Read paradigm from a dict
		return read_paradigm_dict(value, morph_type, use_defaults=True)
	elif (type(value) == list) and (type(value[0]) == dict):
		# Read a list of paradigms from a list of dicts
		return [read_paradigm_dict(d, morph_type, use_defaults) for d in value]
	elif (type(value) == list) and (type(value[0]) == str):
		# Expand a list of paradigms from a list of strings
		return [paradigm_from_string(s, morph_type, use_defaults=True) for s in value]
	elif type(value) == str:
		# Expand a paradigm from a stingle string
		return paradigm_from_string(value, morph_type, use_defaults=True)
	else:
		Logger.error("unable to read MnE paradigm: " + str(value))

# Read a paradigm from a paradigm dict
def read_paradigm_dict(value, morph_type, use_defaults):
	if morph_type == "noun":
		return read_noun(value)
	elif morph_type == "adj":
		return read_adj(value, use_defaults)
	else:
		return read_verb(value)

def paradigm_from_string(string, morph_type, use_defaults):
	if morph_type == "noun":
		plural = mne_morphology.default_plural(string)
		return Paradigm_MnE_N(string, plural)
	elif morph_type == "adj":
		if use_defaults:
			comp = mne_morphology.default_comparative(string)
			sup = mne_morphology.default_superlative(string)
		else:
			comp = None
			sup = None

		return Paradigm_MnE_A(string, comp, sup)
	else:
		past = mne_morphology.default_past(string)
		past_participle = mne_morphology.default_past_participle(string)
		return Paradigm_MnE_V(string, past, past_participle)

def read_noun(value):
	singular = value["lemma"]

	if "plural" in value:
		plural = value["plural"]
	else:
		plural = mne_morphology.default_plural(singular)

	return Paradigm_MnE_N(singular, plural)

def read_adj(value, use_defaults):
	lemma = value["lemma"]

	if "comparative" in value:
		comp = value["comparative"]
	elif use_defaults:
		comp = mne_morphology.default_comparative(lemma)
	else:
		comp = None

	if "superlative" in value:
		sup = value["superlative"]
	elif use_defaults:
		sup = mne_morphology.default_superlative(lemma)
	else:
		sup = None

	return Paradigm_MnE_A(lemma, comp, sup)

def read_verb(value):
	lemma = value["lemma"]

	if "past" in value:
		past = value["past"]
	else:
		past = default_past(lemma)

	if "past-participle" in value:
		ppart = value["past-participle"]
	else:
		ppart = mne_morphology.default_past_participle(lemma)

	return Paradigm_MnE_V(lemma, past, ppart)
