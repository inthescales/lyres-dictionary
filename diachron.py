import getopt
import sys

import src.diachron.orth_oe as old_english
import src.diachron.me as middle_english
import src.diachron.modernize_oe as modernize_oe
import src.diachron.table as table
import src.helpers as helpers

def get_clusters(word):
    cluster = []
    clusters = []
    polarity = None

    def open_cluster(char):
        nonlocal cluster, clusters, polarity

        polarity = char in vowels
        cluster = [char]
        print("New cluster: " + char + " (" + str(polarity) + ")")

    def continue_cluster(char):
        nonlocal cluster

        cluster += char
        print("Adding " + char)

    def close_cluster():
        nonlocal cluster, clusters, polarity

        clusters.append(cluster)
        print("Finished cluster '" + str(cluster) + "'")
        cluster = []
        polarity = None

    for i in range(0, len(word)):
        print("char '" + word[i] + "'")

        if cluster != []:
            if polarity == (word[i] in vowels):
                continue_cluster(word[i])
            else:
                close_cluster()

        if cluster == []:
            open_cluster(word[i])

    close_cluster()

    return clusters

def run(input):
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
        phonemes = old_english.get_old_english_phonemes(input)
        oe_phonemes.append(phonemes)

    me_phonemes = []
    modern_forms = []
    for oe in oe_phonemes:
        transformed = modernize_oe.me_phonemes(oe)
        me_phonemes.append(transformed)

        spelling = modernize_oe.orthography(transformed)
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

def test():
    test_data = [
        ["cild", "tʃild", "tʃild"],
        ["dæg", "dæj", "dɛi"],
        ["frēond", "freːond", "freːnd"], # Wiki has "fre͜oːnd" in 1
        ["mēt|an", "meːtɑn", "meːt"],
        ["niht", "nixt", "nixt"],
        ["wicu", "", "weːk"]
    ]

    count_success = 0
    count_failure = 0

    for data in test_data:
        oe_graph = data[0]
        oe_phone = data[1]
        me_phone = data[2]

        oe_phone_proc = old_english.get_old_english_phonemes(oe_graph)
        me_phone_proc = middle_english.phonemes_from_oe_3(oe_phone_proc)

        oe_phone_test = "".join([x.value for x in oe_phone_proc])
        me_phone_test = "".join([x.value for x in me_phone_proc])

        if oe_phone != oe_phone_test:
            print("FAILED : OE phonemes : " + oe_phone + " != " + oe_phone_test)
            count_failure += 1
            continue
        if me_phone != me_phone_test:
            print("FAILED : ME phonemes : " + me_phone + " != " + me_phone_test)
            count_failure += 1
            continue
        else:
            print("SUCCEEDED : " + oe_graph + " -> " + oe_phone + " -> " + me_phone)
            count_success += 1
            continue

    print("\nTESTS FINISHED")
    print("SUCCESS: " + str(count_success))
    print("FAILURE: " + str(count_failure))

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

    run(input)
    # test()
