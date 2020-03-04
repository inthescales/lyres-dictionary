import sys

from src.models import Morph, Word, check_req
from src.morphothec import Morphothec

morphothec = Morphothec(["data/morphs-latin.json"])

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
            series.elements[i].append(word.compose())
            
            root_morph = morphothec.morph_for_key[root]
            suffix_morph = morphothec.morph_for_key[suffix]
            if "requires" in suffix_morph:
                referents = {"preceding": root_morph}
                series.is_valid[i].append(check_req(morphothec.morph_for_key[suffix], referents))
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
            series.elements[i].append(word.compose())

            prefix_morph = morphothec.morph_for_key[prefix]
            root_morph = morphothec.morph_for_key[root]
            suffix_morph = morphothec.morph_for_key[suffix]
            if "requires" in suffix_morph or "requires" in prefix_morph:
                suffix_referents = {"preceding": root_morph}
                prefix_referents = {"following": root_morph}
                series.is_valid[i].append(
                    (check_req(morphothec.morph_for_key[suffix], suffix_referents)
                     and check_req(morphothec.morph_for_key[prefix], prefix_referents))
                )
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
            series.elements[i].append(word.compose())

            prefix_morph = morphothec.morph_for_key[prefix]
            verb_morph = morphothec.morph_for_key[verb]
            if "requires" in prefix_morph:
                prefix_referents = {"following": verb_morph}
                series.is_valid[i].append(check_req(morphothec.morph_for_key[prefix], prefix_referents))
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

#test_series = series_root_suffix(morphothec.type_morphs["verb"], morphothec.filter_appends_to("verb"), morphothec)
#test_series = series_verb("jungere", 
#                          morphothec.filter_type("prep", { "has-tag": "verbal" }),
#                          morphothec.filter_appends_to("verb"),
#                          morphothec)
test_series = series_prefix_verb(morphothec.filter_type("prep", { "has-tag": "verbal" }),
                                 morphothec.filter_type("verb"),
                                 morphothec)

print(getHTML(test_series))
