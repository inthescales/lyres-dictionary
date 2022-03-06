import sys

from src.models.morph import Morph
from src.models.word import Word
from src.models.environment import Environment

import src.composer as composer
from src.morphothec import Morphothec

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
            series.elements[i].append(composer.get_form(word))
            
            root_morph, suffix_morph = word.morphs[0], word.morphs[1]
            if "requires" in suffix_morph.morph:
                env = Environment(None, root_morph, None, None)
                valid = suffix_morph.meets_requirements(env, filter_frequency=False)
                series.is_valid[i].append(valid)
            else:
                series.is_valid[i].append(True)

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
            series.elements[i].append(composer.get_form(word))

            prefix_morph, root_morph, suffix_morph = word.morphs[0], word.morphs[1], word.morphs[2]
            if "requires" in suffix_morph.morph or "requires" in prefix_morph.morph:
                suffix_env = Environment(prefix_morph, root_morph, None, None)
                prefix_env = Environment(None, None, root_morph, suffix_morph)
                valid = suffix_morph.meets_requirements(suffix_env, filter_frequency=False)
                valid = valid and prefix_morph.meets_requirements(prefix_env, filter_frequency=False)
                series.is_valid[i].append(valid)
            else:
                series.is_valid[i].append(True)

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
            series.elements[i].append(composer.get_form(word))

            prefix_morph, verb_morph = word.morphs[0], word.morphs[1]
            if "requires" in prefix_morph.morph:
                env = Environment(None, None, verb_morph, None)
                series.is_valid[i].append(prefix_morph.meets_requirements(env, filter_frequency=False))
            else:
                series.is_valid[i].append(True)

            series.is_rare[i].append(suffix_morph.has_tag("rare"))
    
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
            series.elements[i].append(composer.get_form(word))
            
            prefix_morph, root_morph, suffix_morph = word.morphs[0], word.morphs[1], word.morphs[2]
            if "requires" in suffix_morph.morph or "requires" in prefix_morph.morph:
                suffix_env = Environment(prefix_morph, root_morph, None, None)
                prefix_env = Environment(None, None, root_morph, suffix_morph)
                valid = suffix_morph.meets_requirements(suffix_env, filter_frequency=False)
                valid = valid and prefix_morph.meets_requirements(prefix_env, filter_frequency=False)
                series.is_valid[i].append(valid)
            else:
                series.is_valid[i].append(True)

            series.is_rare[i].append(prefix_morph.has_tag("rare") or suffix_morph.has_tag("rare"))
    
    return series

def getHTML(series):
    
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

test_series = series_root_suffix(morphothec.filter_type("noun", "latin"),
                                 ["-ine"],
                                 morphothec)

#test_series = series_verb("tarassein", 
#                          morphothec.filter_prepends_to("verb", "greek", { "has-type": "prep" }),
#                          morphothec.filter_appends_to("verb", language="greek"),
#                          morphothec)

# test_series = series_prefix_verb(morphothec.filter_type("prep", "latin"),
#                                  morphothec.filter_type("verb"),
#                                  morphothec)

#test_series = series_noun_circumfix(morphothec.filter_prepends_to("noun", "greek"),
#                                    morphothec.filter_type("noun", "greek"),
#                                    "-ic",
#                                    morphothec)


print(getHTML(test_series))
