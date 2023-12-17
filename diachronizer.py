import getopt
import sys

import src.diachronizer.language.oe_phonology as oe_phonology
import src.diachronizer.language.me_phonology as me_phonology
import src.diachronizer.language.ne_orthography as ne_orthography
import src.diachronizer.table as table
import src.helpers as helpers

def form_from_oe(oe_form, config=[], verbose=False):
    oe_phonemes = oe_phonology.from_oe_written(oe_form)
    me_phonemes = me_phonology.from_oe_phonemes(oe_phonemes, config, verbose)
    modern_form = ne_orthography.from_me_phonemes(me_phonemes, config)

    return modern_form

# Table Drawing =================================

def make_table(input):
    inputs = [
        "stel|an",
        "bāt",
        "cȳð|an",
        "frēod",
        "heofon",
        "mete",
        "ċild",
        "dæg",
        "frēond",
        "nama",
        "eorðe",
        "cniht",
        "mægden",
        "hund",
        "bryċġ",
        "gāst",
        "gōd",
        "cēp|an",
        "cēpte",
        "mæt|an",
        "mētte",
        "niht",
        "hlæhh|an",
        "tōh",
        "mann",
        "lamb",
        "nacod"
    ]

    oe_phonemes = []
    for input in inputs:
        phonemes = oe_phonology.from_oe_written(input)
        oe_phonemes.append(phonemes)

    me_phonemes = []
    for oe in oe_phonemes:
        phonemes = me_phonology.from_oe_phonemes(oe)
        me_phonemes.append(phonemes)

    modern_forms = []
    for me in me_phonemes:
        spelling = ne_orthography.from_me_phonemes(me)
        modern_forms.append(spelling)

    oe_output = ["/" + "".join([x.value for x in word]) + "/" for word in oe_phonemes]
    me_output = ["/" + "".join([x.value for x in word]) + "/" for word in me_phonemes]
    output_table = table.make_table([
        table.TableColumn("OE written", inputs),
        table.TableColumn("OE phonemes", oe_output),
        table.TableColumn("ME phonemes", me_output),
        table.TableColumn("Modern form", modern_forms),
    ])

    print(output_table)

# Process command line input
if __name__ == '__main__' and len(sys.argv) > 0:
    
    input = None
    
    # Error cases
    def error_no_input():
        print("Error: Must provide input word")
        sys.exit(1)
    
    # Get args
    try:
        opts, params = getopt.getopt(sys.argv[1:], "w:", ["word="])
    except getopt.GetoptError:
        error_no_input()
        sys.exit(2)

    # Process args
    for opt, arg in opts:
        if opt in ["-w", "--word"]:
            input = arg

    make_table(input)
    # test()
