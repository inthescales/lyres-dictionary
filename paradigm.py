import sys

from src.models.morph import Morph
from src.models.word import Word
from src.models.environment import Environment

import src.composer as composer
from src.morphothec import Morphothec

morphothec = Morphothec(["data/morphs-greek.json"])

class Series:
    def __init__(self):
        self.x_labels = []
        self.y_labels = []
        self.elements = []
        self.is_valid = []

def series_root_suffix(roots, suffixes, morphothec):
    series = Series()
    series.x_labels = suffixes
    series.y_labels = roots
    
    for i, root in enumerate(roots):
        series.elements.append([])
        series.is_valid.append([])
        for j, suffix in enumerate(suffixes):
            word = Word(morphothec)
            word.set_keys([root, suffix])
            series.elements[i].append(composer.get_form(word))
            
            root_morph, suffix_morph = word.morphs[0], word.morphs[1]
            if "requires" in suffix_morph.morph:
                env = Environment(None, root_morph, None, None)
                valid = suffix_morph.meets_requirements(env)
                series.is_valid[i].append(valid)
            else:
                series.is_valid[i].append(True)
    
    return series

def series_verb(root, prefixes, suffixes, morphothec):
    series = Series()
    series.x_labels = suffixes
    series.y_labels = prefixes
    
    for i, prefix in enumerate(prefixes):
        series.elements.append([])
        series.is_valid.append([])
        for j, suffix in enumerate(suffixes):
            word = Word(morphothec)
            word.set_keys([prefix, root, suffix])
            series.elements[i].append(composer.get_form(word))

            prefix_morph, root_morph, suffix_morph = word.morphs[0], word.morphs[1], word.morphs[2]
            if "requires" in suffix_morph.morph or "requires" in prefix_morph.morph:
                suffix_env = Environment(prefix_morph, root_morph, None, None)
                prefix_env = Environment(None, None, root_morph, suffix_morph)
                valid = suffix_morph.meets_requirements(suffix_env)
                valid = valid and prefix_morph.meets_requirements(prefix_env)
                series.is_valid[i].append(valid)
            else:
                series.is_valid[i].append(True)
                
    return series

def series_prefix_verb(prefixes, verbs, morphothec):
    series = Series()
    series.x_labels = verbs
    series.y_labels = prefixes
    
    for i, prefix in enumerate(prefixes):
        series.elements.append([])
        series.is_valid.append([])
        for j, verb in enumerate(verbs):
            word = Word(morphothec)
            word.set_keys([prefix, verb])
            series.elements[i].append(composer.get_form(word))

            prefix_morph, verb_morph = word.morphs[0], word.morphs[1]
            if "requires" in prefix_morph.morph:
                env = Environment(None, None, verb_morph, None)
                series.is_valid[i].append(prefix_morph.meets_requirements(env))
            else:
                series.is_valid[i].append(True)
    
    return series

def getHTML(series):
    
    tdstyle = "border: 1px solid black; padding: 8px;"
    def cell(header, valid, contents):
        tag = "td"
        color = "black"
        
        if header: tag = "th";
        if not valid: color = "red"
            
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
        output += cell(True, True, label) + "\n"
    output += "</tr>\n"
    
    # Rows
    for i, row in enumerate(series.elements):
        output += "<tr>\n"
        output += cell(True, True, series.y_labels[i]) + "\n"
        for j, entry in enumerate(row):
            output += cell(False, series.is_valid[i][j], entry) + "\n"
        output += "</tr>\n"
    
    # Closing
    output += "</table>\n"
    output += "</body>\n"
    
    return output

test_series = series_root_suffix(morphothec.filter_type("noun", language="greek"),
                                 morphothec.filter_appends_to("noun", language="greek"),
                                 morphothec)
#test_series = series_root_suffix(morphothec.filter_type("verb"),
#                                 morphothec.filter_appends_to("verb"),
#                                 morphothec)
#test_series = series_verb("jungere", 
#                          morphothec.filter_type("prep", { "has-tag": "verbal" }),
#                          morphothec.filter_appends_to("verb"),
#                          morphothec)
# test_series = series_prefix_verb(morphothec.filter_type("prep", "latin", { "has-tag": "verbal" }),
#                                  morphothec.filter_type("verb"),
#                                  morphothec)

print(getHTML(test_series))
