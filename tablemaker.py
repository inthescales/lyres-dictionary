import getopt
import sys

import src.diachronizer.diachronizer as diachronizer
import src.diachronizer.engine.helpers as helpers
from src.diachronizer.engine.helpers import Config
import src.tablemaker.table as table

# Table Drawing =================================

def make_table_oe(input):
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

    config = Config(locked=True)

    oe_phonemes = []
    for input in inputs:
        phonemes = diachronizer.oe_orth_to_oe_phone(input, config)
        oe_phonemes.append(phonemes)

    me_phonemes = []
    for oe in oe_phonemes:
        phonemes = diachronizer.oe_phone_to_me_phone(oe, config)
        me_phonemes.append(phonemes)

    modern_forms = []
    for me in me_phonemes:
        spelling = diachronizer.me_phone_to_ne_orth(me, config)
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

    make_table_oe(input)
    # test()
