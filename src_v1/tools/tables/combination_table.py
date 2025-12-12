import src.generation.composer as composer

from src.models.environment import Environment
from src.models.morph import Morph
from src.models.word import Word
from src.morphs.morphothec import Morphothec

morphothec = Morphothec("data/")

class Series:
    def __init__(self):
        self.x_labels = []
        self.y_labels = []
        self.elements = []
        self.is_valid = []
        self.is_rare = []

# Table of roots and their suffixes
def series_root_suffix(roots, suffixes, morphothec):
    series = Series()
    series.x_labels = suffixes
    series.y_labels = roots
    
    for i, root in enumerate(roots):
        series.elements.append([])
        series.is_valid.append([])
        series.is_rare.append([])
        for j, suffix in enumerate(suffixes):
            word = Word(morphothec)
            word.set_keys([root, suffix])
            root_morph, suffix_morph = word.morphs[0], word.morphs[1]

            valid = True
            if "requires" in suffix_morph.morph:
                env = Environment(None, root_morph, None, None)
                valid = suffix_morph.meets_requirements(env, filter_frequency=False)
            
            series.elements[i].append(composer.get_form(word))
            series.is_valid[i].append(valid)
            series.is_rare[i].append(suffix_morph.has_tag("rare"))
    
    return series

# Table of single verb root with combinations of prefixes and suffixes
def series_verb(root, prefixes, suffixes, morphothec):
    series = Series()
    series.x_labels = suffixes
    series.y_labels = prefixes
    
    for i, prefix in enumerate(prefixes):
        series.elements.append([])
        series.is_valid.append([])
        series.is_rare.append([])
        for j, suffix in enumerate(suffixes):
            word = Word(morphothec)
            word.set_keys([prefix, root, suffix])
            prefix_morph, root_morph, suffix_morph = word.morphs[0], word.morphs[1], word.morphs[2]

            valid = True
            if "requires" in suffix_morph.morph or "requires" in prefix_morph.morph:
                suffix_env = Environment(prefix_morph, root_morph, None, None)
                prefix_env = Environment(None, None, root_morph, suffix_morph)
                valid = suffix_morph.meets_requirements(suffix_env, filter_frequency=False) \
                    and prefix_morph.meets_requirements(prefix_env, filter_frequency=False)

            series.elements[i].append(composer.get_form(word))
            series.is_valid[i].append(valid)
            series.is_rare[i].append(prefix_morph.has_tag("rare") or suffix_morph.has_tag("rare"))
                
    return series

# Table of verb roots with prefixes
def series_prefix_verb(prefixes, verbs, morphothec):
    series = Series()
    series.x_labels = verbs
    series.y_labels = prefixes
    
    for i, prefix in enumerate(prefixes):
        series.elements.append([])
        series.is_valid.append([])
        series.is_rare.append([])
        for j, verb in enumerate(verbs):
            word = Word(morphothec)
            word.set_keys([prefix, verb])
            prefix_morph, verb_morph = word.morphs[0], word.morphs[1]

            valid = True
            if "requires" in prefix_morph.morph:
                env = Environment(None, None, verb_morph, None)
                valid = prefix_morph.meets_requirements(env, filter_frequency=False)

            series.elements[i].append(composer.get_form(word))
            series.is_valid[i].append(valid)
            series.is_rare[i].append(prefix_morph.has_tag("rare") or verb_morph.has_tag("rare"))
    
    return series

# Table of nouns in circumfixes with different prefixes, one suffix.
def series_noun_circumfix(prefixes, roots, suffix, morphothec):
    series = Series()
    series.x_labels = roots
    series.y_labels = prefixes
    
    for i, prefix in enumerate(prefixes):
        series.elements.append([])
        series.is_valid.append([])
        series.is_rare.append([])
        for j, root in enumerate(roots):
            word = Word(morphothec)
            word.set_keys([prefix, root, suffix])
            prefix_morph, root_morph, suffix_morph = word.morphs[0], word.morphs[1], word.morphs[2]
            
            valid = True
            if "requires" in suffix_morph.morph or "requires" in prefix_morph.morph:
                suffix_env = Environment(prefix_morph, root_morph, None, None)
                prefix_env = Environment(None, None, root_morph, suffix_morph)
                valid = suffix_morph.meets_requirements(suffix_env, filter_frequency=False) \
                    or prefix_morph.meets_requirements(prefix_env, filter_frequency=False)

            series.elements[i].append(composer.get_form(word))
            series.is_valid[i].append(valid)
            series.is_rare[i].append(prefix_morph.has_tag("rare") or suffix_morph.has_tag("rare"))
    
    return series

def getHTML(series):
    # TODO: combine this with table.py
    
    tdstyle = "border: 1px solid black; padding: 8px;"
    def cell(header, valid, rare, contents):
        tag = "td"
        color = "black"
        
        if header: tag = "th";
        if not valid: color = "red"
        if rare: color = "blue"
            
        style = "color: " + color + "; " + tdstyle
        return "<" + tag + " style=\"" + style + "\">" + contents + "</" + tag + ">"
    
    #Opening
    output = "<body>\n"
    style = '"border: 1px solid black;"'
    if not style:
        output += "<table>\n"
    else:
        output += "<table style=" + style + ">\n"
    
    # X-axis labels
    output += "<tr>\n"
    output += "<td></td>\n"
    for label in series.x_labels:
        output += cell(True, True, False, label) + "\n"
    output += "</tr>\n"
    
    # Rows
    for i, row in enumerate(series.elements):
        output += "<tr>\n"
        output += cell(True, True, False, series.y_labels[i]) + "\n"
        for j, entry in enumerate(row):
            output += cell(False, series.is_valid[i][j], series.is_rare[i][j], entry) + "\n"
        output += "</tr>\n"
    
    # Closing
    output += "</table>\n"
    output += "</body>\n"
    
    return output

def make_table():
    # Hard coded logic until I think of a good way to argument-ize this

    test_series = series_root_suffix(morphothec.filter_type("noun", "old-english"), # ["manus"]
                                    ["-ery"], # morphothec.filter_appends_to("noun", "latin"),
                                    morphothec)

    # test_series = series_verb("tarassein", 
    #                          morphothec.filter_prepends_to("verb", "greek", { "has-type": "prep" }),
    #                          morphothec.filter_appends_to("verb", language="greek"),
    #                          morphothec)

    # test_series = series_prefix_verb(morphothec.filter_prepends_to("verb", "latin", { "has-type": "prep" }),
    #                                  morphothec.filter_type("verb", "latin"),
    #                                  morphothec)

    # test_series = series_noun_circumfix(morphothec.filter_prepends_to("noun", "greek"),
    #                                    morphothec.filter_type("noun", "greek"),
    #                                    "-ic",
    #                                    morphothec)

    return getHTML(test_series)
