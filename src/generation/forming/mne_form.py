import src.language.modern_english.morphology as mne_morphology

from src.utils.logging import Logger

# Structures ===========================

class Paradigm_MnE_N():
	def __init__(self, lemma, plural):
		self.lemma = lemma
		self.plural = plural

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

def read_paradigm(struct, morph_type):
	if morph_type == "noun":
		return read_noun(struct)
	elif morph_type == "adj":
		return read_adjective(struct)
	else:
		return read_verb(struct)

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
		Logger.error("cannot read modern english verb paradigm from a single string")

def read_noun(struct):
	lemma = struct["lemma"]

	if "plural" in struct:
		plural = struct["plural"]
	else:
		plural = mne_morphology.default_plural(lemma)

	return Paradigm_MnE_N(lemma, plural)

def read_adj(struct, use_defaults):
	lemma = struct["lemma"]

	if "comparative" in struct:
		comp = struct["comparative"]
	elif use_defaults:
		comp = mne_morphology.default_comparative(lemma)
	else:
		comp = None

	if "superlative" in struct:
		sup = struct["superlative"]
	elif use_defaults:
		sup = mne_morphology.default_superlative(lemma)
	else:
		sup = None

	return Paradigm_MnE_A(lemma, comp, sup)

def read_verb(struct):
	lemma = struct["lemma"]

	if "past" in struct:
		past = struct["past"]
	else:
		past = default_past(lemma)

	if "past-participle" in struct:
		ppart = struct["past-participle"]
	else:
		ppart = mne_morphology.default_past_participle(lemma)

	return Paradigm_MnE_V(lemma, past, ppart)
