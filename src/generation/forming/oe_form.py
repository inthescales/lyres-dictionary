import src.generation.forming.mne_form as mne_form
import src.utils.helpers as helpers

from src.utils.logging import Logger

# Structures ====================================

# A formset represents a set of linked forms sufficient to represent a morph
# in any way that would be needed (for example, an OE verb in present, past,
# and past-participle forms). It also includes any canonical modern forms derived
# from those forms, some metadata.
# Most form properties are represented as lists to accommodate the possibility
# of alternate forms.
class Formset_OE():
	def __init__(self, type, main, alt):
		self.type = type
		self.main = main
		self.alt = alt

	def __str__(self):
		return "type: " + self.type + "\nmain: " + str(self.main) + "\nalt: " + str(self.alt)

# A form (one or more paradigms), a canon reflex if any (one or more canonsets), and metadata about that form
class Metaform():
	def __init__(self, paradigm, canon, dialect):
		self.paradigm = paradigm
		self.canon = canon
		self.dialect = dialect

	def __str__(self):
		return "paradigm: " + str(self.paradigm) + "\ncanon: " + str(self.canon) + "\ndialect: " + self.dialect

# A canon form (one or more MnE paradigms) and related metadata
class Canonset():
	def __init__(self, dialect, form):
		self.dialect = dialect
		self.form = form

	def __str__(self):
		return "dialect: " + self.dialect + "\nform: " + str(self.form)

# Paradigm for Old English nouns and adjectives
class Paradigm_OE_B():
	def __init__(self, lemma, oblique):
		self.lemma = lemma
		self.oblique = oblique

	def __str__(self):
		return "lemma: " + str(self.lemma) + ", oblique: " + str(self.oblique)

# Paradigm Old English for verbs
class Paradigm_OE_V():
	def __init__(self, infinitive, past, past_participle):
		self.infinitive = infinitive
		self.past = past
		self.past_participle = past_participle

	def __str__(self):
		return "infinitive: " + str(self.infinitive) + ", past: " + str(self.past) + ", past-participle: " + str(self.past_participle)

# Parsing =============================================

# Read an Old English formset
def read(struct, morph_type):
	if type(struct) == str:
		# Expand a single string into a paradigm and metaform
		main = Metaform(paradigm_from_string(struct, morph_type), None, default_oe_dialect)
		return Formset_OE(morph_type, main, None)
	elif type(struct) == list and len(struct) > 0 and type(struct[0]) == str:
		# Expand a list of strings into a metaform with multiple paradigms
		main = Metaform([paradigm_from_string(f, morph_type) for f in struct], None, default_oe_dialect)
		return Formset_OE(morph_type, main, None)
	elif type(struct) == dict:
		if "form" in struct:
			# Read a metaform dict
			main = read_metaform(struct, morph_type)
			return Formset_OE(morph_type, main, None)
		elif "main" in struct and "alt" in struct:
			# Read a multiform dict
			return read_multiform(struct, morph_type)
		else:
			# Expand a single paradigm dict into a metaform
			main = Metaform(read_paradigm(struct), None, default_oe_dialect)
			return Formset_OE(morph_type, main, None)

	Logger.error("invalid formset: "+ str(struct))

# Read a multiform (one or more metaforms)
def read_multiform(struct, morph_type):
	main = read_metaform(struct["main"], morph_type)

	if type(struct["alt"]) == list:
		alt = [read_metaform(a) for a in struct["alt"]]
	else:
		alt = [read_metaform(struct["alt"])]

	return Formset_OE(morph_type, main, alt)

# Read metaform
def read_metaform(struct, morph_type):
	if "dialect" in struct:
		dialect = struct["dialect"]
	else:
		dialect = default_oe_dialect

	if type(struct["form"]) == dict:
		# Read a paradigm dict
		raw = read_paradigm(struct["form"])
	elif (type(struct["form"]) == list) and (type(struct["form"][0]) == dict):
		# Read a list of paradigm dicts
		raw = [read_paradigm(f, morph_type) for f in struct["form"]]
	elif (type(struct["form"]) == list) and (type(struct["form"][0]) == str):
		# Expand a list of strings into a list of paradigms
		raw = [paradigm_from_string(f, morph_type) for f in struct["form"]]
	elif type(struct["form"]) == str:
		# Expand a single string into a paradigm
		raw = paradigm_from_string(struct["form"], morph_type)
	else:
		Logger.error("couldn't read OE paradigm '" + str(struct["form"]) + "'")

	# Read canon form if present, resulting in one or more canonsets
	if "canon" in struct:
		if type(struct["canon"]) == dict:
			if "form" in struct["canon"]:
				# Read canonset from full canonset dict
				canon = read_canonset(struct["canon"], morph_type)
			else:
				# Create canonset from paradigm dict
				canon = Canonset(default_me_dialect, mne_form.read_paradigm(struct["canon"], morph_type))
		elif (type(struct["canon"]) == list) and (type(struct["canon"][0]) == dict):
			if "form" in struct["canon"][0]:
				# Create list of canonsets from list of canonset dicts
				canon = [read_canonset(c, morph_type) for c in struct["canon"]]
			else:
				# Create a list of canonsets from a list of paradigm dicts
				canon_forms = [mne_form.read_paradigm(d, morph_type) for d in struct["canon"]]
				canon = [Canonset(default_me_dialect, form) for form in canon_forms]
		elif (type(struct["canon"]) == list) and (type(struct["canon"][0]) == str):
			# Create a list of canonsets from a list of strings
			canon_forms = [mne_form.paradigm_from_string(s, morph_type, use_defaults=True) for s in struct["canon"]]
			canon = [Canonset(default_me_dialect, form) for form in canon_forms]
		elif type(struct["canon"]) == str:
			# Create a single canonset from a single string
			canon = Canonset(default_me_dialect, mne_form.paradigm_from_string(struct["canon"], morph_type, use_defaults=True))
		else:
			Logger.error("couldn't read canonset: " + str(struct["canon"]))

		return Metaform(raw, canon, dialect)
	else:
		return Metaform(raw, None, dialect)

def read_paradigm(struct):
	if "lemma" in struct:
		return read_paradigm_basic(struct)
	elif "infinitive" in struct:
		return read_paradigm_verb(struct)
	else:
		Logger.error("unrecognized OE paradigm: "+ str(struct))

def read_paradigm_basic(struct):
	if "oblique" in struct:
		return Paradigm_OE_B(struct["lemma"], struct["oblique"])
	else:
		return Paradigm_OE_B(struct["lemma"], default_oblique(struct["lemma"]))

def read_paradigm_verb(struct):
	return Paradigm_OE_V(struct["infinitive"], struct["past"], struct["past-participle"])

# Read a canonset dict, resulting in one or more canonsets
def read_canonset(struct, morph_type):
	if type(struct["form"]) == dict:
		# Read paradigm from a dict
		form = mne_form.read_paradigm(struct["form"], morph_type)
	elif (type(struct["form"]) == list) and (type(struct["form"][0]) == dict):
		# Read a list of paradigms from a list of dicts
		form = [mne_form.read_paradigm(f, morph_type) for f in struct["form"]]
	elif (type(struct["form"]) == list) and (type(struct["form"][0]) == str):
		# Expand a list of paradigms from a list of strings
		form = [mne_form.paradigm_from_string(f, morph_type, use_defaults=True) for f in struct["form"]]
	elif type(struct["form"]) == str:
		# Expand a paradigm from a stingle string
		form = mne_form.paradigm_from_string(struct["form"], morph_type, use_defaults=True)
	else:
		Logger.error("unable to read canonset: " + str(struct))

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

