import src.generation.forming.mne_form as mne_form
import src.utils.helpers as helpers

from src.utils.logging import Logger

# TODO: Make separate modern english formsets
# N - singular, plural
# A - lemma, comparative, superlative
# V - present, past, past-participle

# Structures ====================================

# A formset represents a set of linked forms sufficient to represent a morph
# in any possible way (for example, an OE verb in present, past, and past-participle
# forms).
# It also includes any canonical modern forms derived from those forms, and
# It does NOT take alternate forms into account - this object is created to represent
# the specific set of forms that will be used.
class Formset_OE():
	def __init__(self, type, main, alt):
		self.type = type
		self.main = main
		self.alt = alt

	def __str__(self):
		return "type: " + self.type + "\nmain: " + str(self.main) + "\nalt: " + str(self.alt)

# A form and metadata about that form
class Metaform():
	def __init__(self, paradigm, canon, dialect):
		self.paradigm = paradigm
		self.canon = canon
		self.dialect = dialect

	def __str__(self):
		return "paradigm: " + str(self.paradigm) + "\ncanon: " + str(self.canon) + "\ndialect: " + self.dialect

# Paradigm for nouns and adjectives
class Paradigm_OE_B():
	def __init__(self, lemma, oblique):
		self.lemma = lemma
		self.oblique = oblique

	def __str__(self):
		return "lemma: " + str(self.lemma) + ", oblique: " + str(self.oblique)

# Paradigm for verbs
class Paradigm_OE_V():
	def __init__(self, infinitive, past, past_participle):
		self.infinitive = infinitive
		self.past = past
		self.past_participle = past_participle

	def __str__(self):
		return "infinitive: " + str(self.infinitive) + ", past: " + str(self.past) + ", past-participle: " + str(self.past_participle)

# A canon form and related metadata
class Canonset():
	def __init__(self, dialect, form):
		self.dialect = dialect
		self.form = form

	def __str__(self):
		return "dialect: " + self.dialect + "\nform: " + str(self.form)

# Parsing =============================================

# Read an Old English form structure.
def read(struct, morph_type, config):
	return read_head(struct, morph_type, config)

def read_head(struct, morph_type, config):
	if type(struct) == str:
		return Metaform(paradigm_from_string(struct, morph_type), None, default_oe_dialect)
	if type(struct) == dict:
		if "form" in struct:
			main = read_metaform(struct, morph_type, config)
			return Formset_OE(morph_type, main, None)
		elif "main" in struct and "alt" in struct:
			return read_multiform(struct, morph_type, config)
		else:
			return read_paradigm(struct, config)

	Logger.error("invalid form-oe head")

def read_multiform(struct, morph_type, config):
	main = read_metaform(struct["main"], morph_type, config)

	if type(struct["alt"]) == list:
		alt = [read_metaform(a, config) for a in struct["alt"]]
	else:
		alt = [read_metaform(struct["alt"], config)]

	return Formset_OE(morph_type, main, alt)

def read_metaform(struct, morph_type, config):
	if "dialect" in struct:
		dialect = struct["dialect"]
	else:
		dialect = default_oe_dialect

	# Read form, resulting in one or more paradigms
	if type(struct["form"]) == dict:
		raw = read_paradigm(struct["form"], config)
	elif (type(struct["form"]) == list) and (type(struct["form"][0]) == dict):
		raw = [read_paradigm(f, morph_type) for f in struct["form"]]
	elif (type(struct["form"]) == list) and (type(struct["form"][0]) == str):
		raw = [paradigm_from_string(f, morph_type) for f in struct["form"]]
	else:
		raw = paradigm_from_string(struct["form"], morph_type)

	# Read canon form if present, resulting in one or more canonsets
	if "canon" in struct:
		if type(struct["canon"]) == dict:
			if "form" in struct["canon"]:
				# Read canonset from full canonset dict
				canon = read_canonset(struct["canon"], morph_type, config)
			else:
				# Create canonset from paradigm dict
				canon = Canonset(default_me_dialect, mne_form.read_paradigm(struct["canon"], morph_type))
		elif (type(struct["canon"]) == list) and (type(struct["canon"][0]) == dict):
			if "form" in struct["canon"][0]:
				# Create list of canonsets from list of canonset dicts
				canon = [read_canonset(c, morph_type, config) for c in struct["canon"]]
			else:
				# Create a list of canonsets from a list of paradigm dicts
				canon_forms = [mne_form.read_paradigm(d, morph_type) for d in struct["canon"]]
				canon = [Canonset(default_me_dialect, form) for form in canon_forms]
		elif (type(struct["canon"]) == list) and (type(struct["canon"][0]) == str):
			# Create a list of canonsets from a list of strings
			canon_forms = [mne_form.paradigm_from_string(s, morph_type, use_defaults=True) for s in struct["canon"]]
			canon = [Canonset(default_me_dialect, form) for form in canon_forms]
		else:
			# Create a single canonset from a single string
			canon = Canonset(default_me_dialect, mne_form.paradigm_from_string(struct["canon"], morph_type, use_defaults=True))

		return Metaform(raw, canon, dialect)
	else:
		return Metaform(raw, dialect)

def read_paradigm(struct, config):
	if "lemma" in struct:
		return read_paradigm_basic(struct, config)
	elif "infinitive" in struct:
		return read_paradigm_verb(struct, config)
	else:
		Logger.error("unrecognized paradigm")

def read_paradigm_basic(struct, config):
	if "oblique" in struct:
		return Paradigm_OE_B(struct["lemma"], struct["oblique"])
	else:
		return Paradigm_OE_B(struct["lemma"], default_oblique(struct["lemma"]))

def read_paradigm_verb(struct, config):
	return Paradigm_OE_V(struct["infinitive"], struct["past"], struct["past-participle"])

# Read a canonset dict, resulting in one or more canonsets
# Assumes that the passed value is a dict
def read_canonset(struct, morph_type, config):
	if type(struct["form"]) == dict:
		form = mne_form.read_paradigm(struct["form"], morph_type)
	elif (type(struct["form"]) == list) and (type(struct["form"][0]) == dict):
		form = [mne_form.read_paradigm(f, morph_type) for f in struct["form"]]
	elif (type(struct["form"]) == list) and (type(struct["form"][0]) == str):
		form = [mne_form.paradigm_from_string(f, morph_type, use_defaults=True) for f in struct["form"]]
	else:
		form = mne_form.paradigm_from_string(struct["form"], morph_type, use_defaults=True)

	if "dialect" in struct:
		dialect = struct["dialect"]
	else:
		dialect = default_me_dialect

	return Canonset(dialect, form)

# Helpers ============================

default_oe_dialect = "unspecified"
default_me_dialect = "unspecified"

def default_oblique(lemma):
	if not helpers.is_vowel(lemma[-1], y_is_vowel=True):
		return lemma + "|e"
	else:
		return lemma

def paradigm_from_string(string, morph_type):
	if morph_type in ["noun", "adj"]:
		return Paradigm_OE_B(string, default_oblique(string))
	else:
		Logger.error("cannot generate paradigm from string with type " + morph_type)

