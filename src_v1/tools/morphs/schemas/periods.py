latin_periods = [
	"classical",
	"vulgar",
	"medieval",
	"modern"
]

greek_periods = [
	"classical",
	"medieval",
	"modern"
]

old_english_periods = [
	"old",
	"middle",
	"early-modern",
	"modern"
]

period_for_language = {
	"latin": latin_periods,
	"greek": greek_periods,
	"old-english": old_english_periods,
	"modern-english": []
}

default_for_language = {
	"latin": "classical",
	"greek": "classical",
	"old-english": "old"
}

def periods_for(language):
	if language in period_for_language:
		return period_for_language[language]

	return []

def default_period_for(language):
	if language in default_for_language:
		return default_for_language[language]

	return None