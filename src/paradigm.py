import sys
sys.path.append(".")

from models import Morph, Word, check_req
from morphary import Morphary

morphary = Morphary(["data/morphs-latin.json"])

class Series:
    def __init__(self):
        self.x_labels = []
        self.y_labels = []
        self.elements = []
        self.is_valid = []

def series_root_suffix(roots, suffixes, morphary):
    series = Series()
    series.x_labels = suffixes
    series.y_labels = roots
    
    for i, root in enumerate(roots):
        series.elements.append([])
        series.is_valid.append([])
        for j, suffix in enumerate(suffixes):
            word = Word(morphary)
            word.set_keys([root, suffix])
            series.elements[i].append(word.compose())
            
            root_morph = morphary.morph_for_key[root]
            suffix_morph = morphary.morph_for_key[suffix]
            if "requires" in suffix_morph:
                referents = {"preceding": root_morph}
                series.is_valid[i].append(check_req(morphary.morph_for_key[suffix], referents))
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

#test_series = series_root_suffix(["canis", "tempus"], ["al", "ous"], morphary)
test_series = series_root_suffix(morphary.type_morphs["noun"], morphary.morphs_from["noun"], morphary)

print(getHTML(test_series))
