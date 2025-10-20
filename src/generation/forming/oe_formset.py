import src.generation.forming.mne_formset as mne_formset
import src.utils.helpers as helpers

from src.utils.logging import Logger

# Structures ====================================

# A formset represents a set of linked forms sufficient to represent a morph
# in any way that would be needed (for example, an OE verb in present, past,
# and past-participle forms). It also includes any canonical modern forms derived
# from those forms, and some metadata.
# Most form properties are represented as lists to accommodate the possibility
# of alternate forms.
class Formset_OE():
	def __init__(self, mtype, main=None, alt=None, all_forms=None):
		self.mtype = mtype
		self.main = main
		self.alt = alt
		self.all = all_forms

		# Initialize with either main and alt, or else a single list of all forms
		if (main == None and all_forms == None):
			Logger.error("Invalid formset initialization. Must provide 'main' or 'all' value")
		elif ((main != None or alt != None) and all_forms != None):
			Logger.error("Invalid formset initialization. Cannot have both 'all'and 'main' or 'alt'")

		if all_forms == None:
			self.all = [main]
			if alt != None:			
				self.all += alt

		self.canon_forms = [form for form in self.all if form.canon != None]

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
	def __init__(self, paradigm, dialect_source, dialect_range):
		self.paradigm = paradigm
		self.source_dialect = dialect_source
		self.dialect_range = dialect_range

	def __str__(self):
		return "paradigm: " + str(self.paradigm) + "\nsource dialect: " + str(self.source) + "\nrange: " + str(self.range)

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

		self.lemma = infinitive

	def __str__(self):
		return "infinitive: " + str(self.infinitive) + ", past: " + str(self.past) + ", past-participle: " + str(self.past_participle)

# Parsing =============================================

# Read an Old English formset
def read(value, morph_type):
	if type(value == dict) and "main" in value and "alt" in value:
		# Read a multiform dict
		return read_multiform(value, morph_type)
	if type(value) == list and all([type(el) == dict and "form" in el for el in value]):
		# Read a list of metaforms
		metaforms = [read_metaform(f, morph_type) for f in value]
		return Formset_OE(morph_type, all_forms=metaforms)
	else:
		# Return a formset with a single main metaform
		metaform = read_metaform(value, morph_type)
		return Formset_OE(morph_type, metaform, None)

	Logger.error("invalid formset: "+ str(value))

# Read a multiform (one or more metaforms)
def read_multiform(value, morph_type):
	main = read_metaform(value["main"], morph_type)
	if type(value["alt"]) == list:
		alt = [read_metaform(a, morph_type) for a in value["alt"]]
	else:
		alt = [read_metaform(value["alt"], morph_type)]

	return Formset_OE(morph_type, main, alt)

# Parse a metaform from any valid input
def read_metaform(value, morph_type):
	if type(value) == dict:
		if "form" in value:
			# Read a metaform dict
			return read_metaform_dict(value, morph_type)
		else:
			# Read a paradigm dict
			paradigm = read_paradigm(value, morph_type)
			return Metaform(paradigm, None, default_oe_dialect)
	elif type(value) == str:
		# Expand a single string into a paradigm
		paradigm = paradigm_from_string(value, morph_type)
		return Metaform(paradigm, None, default_oe_dialect)
	elif type(value) == list and len(value) > 0 and type(value[0]) == str:
		# Expand a list of strings into a metaform with multiple paradigms
		paradigms = [paradigm_from_string(f, morph_type) for f in value]
		return Metaform(paradigms, None, default_oe_dialect)
	elif type(value) == list and len(value) > 0 and type(value[0]) == dict:
		# Expand a list of paradigms into a metaform with multiple paradigms
		paradigms = [read_paradigm(f, morph_type) for f in value]
		return Metaform(paradigms, None, default_oe_dialect)
	else:
		Logger.error("couldn't read OE metaform: " + str(value))

# Read metaform from a metaform dict
def read_metaform_dict(value, morph_type):
	if "dialect" in value:
		dialect = value["dialect"]
	else:
		dialect = default_oe_dialect

	raw = read_paradigm(value["form"], morph_type)

	# Read canon form if present, resulting in one or more canonsets
	if "canon" in value:
		canon = read_canonset(value["canon"], morph_type)
	else:
		canon = None

	return Metaform(raw, canon, dialect)

# Paradigms ---------------------------

# Parse a paradigm from any valid type of input
def read_paradigm(value, morph_type):
	if type(value) == dict:
		# Read a paradigm dict
		return read_paradigm_dict(value)
	elif (type(value) == list) and (type(value[0]) == dict):
		# Read a list of paradigm dicts
		return [read_paradigm_dict(f) for f in value]
	elif type(value) == str:
		# Expand a single string into a paradigm
		return paradigm_from_string(value, morph_type)
	elif (type(value) == list) and (type(value[0]) == str):
		# Expand a list of strings into a list of paradigms
		return [paradigm_from_string(f, morph_type) for f in value]
	else:
		Logger.error("couldn't read OE paradigm '" + str(value) + "'")

# Read a paradigm from a paradigm dict
def read_paradigm_dict(value):
	if "lemma" in value:
		return read_paradigm_basic(value)
	elif "infinitive" in value:
		return read_paradigm_verb(value)
	else:
		Logger.error("unrecognized OE paradigm: "+ str(value))

def read_paradigm_basic(value):
	if "oblique" in value:
		return Paradigm_OE_B(value["lemma"], value["oblique"])
	else:
		return Paradigm_OE_B(value["lemma"], default_oblique(value["lemma"]))

def read_paradigm_verb(value):
	past = None
	if "past" in value:
		past = value["past"]

	past_participle = None
	if "past-participle" in value:
		past_participle = value["past-participle"]

	return Paradigm_OE_V(value["infinitive"], past, past_participle)

# Canonset ----------------------------

# Parse a canonset from any valid type of input
def read_canonset(value, morph_type):
	if type(value) == dict:
		if "form" in value:
			return read_canonset_dict(value, morph_type)
		else:
			# Create canonset from paradigm dict
			paradigm = mne_formset.read_paradigm(value, morph_type)
			return Canonset(paradigm, default_me_dialect, default_mne_dialect)
	elif (type(value) == list) and (type(value[0]) == dict):
		if "form" in value[0]:
			# Create list of canonsets from list of canonset dicts
			return [read_canonset_dict(c, morph_type) for c in value]
		else:
			# Create a canonset with multiple paradigms from a list of paradigm dicts
			paradigms = [mne_formset.read_paradigm(d, morph_type) for d in value]
			return Canonset(paradigms, default_me_dialect, default_mne_dialect)
	elif type(value) == str:
		# Create a single canonset from a single string
		return Canonset(mne_formset.paradigm_from_string(value, morph_type, use_defaults=True), default_me_dialect, default_mne_dialect)
	elif (type(value) == list) and (type(value[0]) == str):
		# Create a canonset with multiple paradigms from a list of strings
		canon_forms = [mne_formset.paradigm_from_string(s, morph_type, use_defaults=True) for s in value]
		return Canonset(canon_forms, default_me_dialect, default_mne_dialect)
	else:
		Logger.error("couldn't read canonset: " + str(value))

# Read canonset from full canonset dict
def read_canonset_dict(value, morph_type):
	form = mne_formset.read_paradigm(value["form"], morph_type)

	if "dialect-source" in value:
		source = value["dialect-source"]
	else:
		source = default_me_dialect

	if "dialect-range" in value:
		if type(value["dialect-range"]) == list:
			dialect_range = value["dialect-range"]
		else:
			dialect_range = [value["dialect-range"]]
	else:
		dialect_range = [default_mne_dialect]

	return Canonset(form, source, dialect_range)

# Helpers ============================

default_oe_dialect = "unspecified"
default_me_dialect = "unspecified"
default_mne_dialect = ["standard"]

def default_oblique(lemma):
	def form_oblique(lemma):
		if not helpers.is_vowel(lemma[-1], y_is_vowel=True):
			return lemma + "|e"
		else:
			return lemma

	if type(lemma) == list:
		return [form_oblique(l) for l in lemma]
	else:
		return form_oblique(lemma)

def paradigm_from_string(string, morph_type):
	if morph_type in ["noun", "adj"]:
		return Paradigm_OE_B(string, default_oblique(string))
	elif morph_type == "verb":
		return Paradigm_OE_V(string, None, None)
	else:
		Logger.error("cannot generate paradigm from string with type " + str(morph_type))

