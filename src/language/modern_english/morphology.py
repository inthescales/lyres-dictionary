import src.language.modern_english.joining as joining

def default_plural(lemma):
	print(lemma)
	if lemma[-2:] == "ss":
		return joining.get_joined_form(lemma, "es")
	elif lemma[-1] == "s":
		return joining.get_joined_form(lemma, "es")
	else:
		return joining.get_joined_form(lemma + "s")

def default_comparative(lemma):
	if lemma[-1] == "e":
		return joining.get_joined_form(lemma, "r")
	else:
		return joining.get_joined_form(lemma, "er")

def default_superlative(lemma):
	if lemma[-1] == "e":
		return joining.get_joined_form(lemma, "st")
	else:
		return joining.get_joined_form(lemma, "est")

def default_past(lemma):
	if lemma[-1] == "e":
		return joining.get_joined_form(lemma, "d")
	else:
		return joining.get_joined_form(lemma, "ed")

def default_past_participle(lemma):
	if lemma[-1] == "e":
		return joining.get_joined_form(lemma, "d")
	else:
		return joining.get_joined_form(lemma, "ed")
