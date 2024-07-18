consonants = ["b", "c", "ċ", "cg", "ċġ", "d", "ð", "f", "g", "ġ", "h", "k", "l", "m", "n", "p", "cw", "r", "s", "sċ", "t", "th", "þ", "uu", "w", "ƿ", "x", "z"]
geminates = [x + x for x in consonants if (len(x) == 1)]

vowels = ["a", "ā", "æ", "ǣ", "e", "ę", "ē", "ea", "ēa", "eo", "ēo", "i", "ī", "ie", "īe", "io", "īo", "o", "ō", "oe", "ōe", "u", "ū", "y", "ȳ"]
front_vowels = ["æ", "ǣ", "i", "ī", "e", "ē"]
back_vowels = ["u", "ū", "a", "ā", "o", "ō"]
short_vowels = ["a", "e", "i", "o", "u", "y", "ea", "eo", "ie", "io", "oe"]
long_vowels = ["ā", "ē", "ī", "ō", "ū", "ȳ", "ēa", "ēo", "īe", "īo", "ōe"]

special_characters = ["'", "|", "."]
