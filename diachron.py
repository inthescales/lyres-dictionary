import getopt
import sys

import src.diachron.orth_oe as old_english
import src.diachron.me as middle_english
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
    oe_phonemes = old_english.get_old_english_phonemes(input)
    me_phonemes = middle_english.phonemes_from_oe(oe_phonemes)
    print([phoneme.value for phoneme in me_phonemes])

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
