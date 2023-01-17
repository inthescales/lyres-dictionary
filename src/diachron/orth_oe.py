consonants = ["b", "c", "ċ", "cg", "d", "ð", "f", "g", "ġ", "h", "k", "l", "m", "n", "p", "cw", "r", "s", "sc", "t", "th", "þ", "uu", "w", "ƿ", "x", "z"]
vowels = ["a", "ā", "æ", "ǣ", "e", "ę", "ē", "ea", "ēa", "eo", "ēo", "i", "ī", "ie", "īe", "io", "īo", "o", "ō", "oe", "ōe", "u", "ū", "y", "ȳ"]

front_vowels = ["æ", "ǣ", "i", "ī", "e", "ē"]
back_vowels = ["u", "ū", "a", "ā", "o", "ō"]

class TrieNode:
    def __init__(self, graph, children=[]):
        self.graph = graph
        self.children = children

graph_trie = {
    "a": TrieNode("a"),
    "ā": TrieNode("ā"),
    "æ": TrieNode("æ"),
    "ǣ": TrieNode("ǣ"),
    "b": TrieNode("b", {"b": TrieNode("bb")}),
    "c": TrieNode("c", {"c": TrieNode("cc", {"g": TrieNode("ccg")}), "g": TrieNode("cg", {"g": TrieNode("cgg")}), "ġ": TrieNode("cġ"), "w": TrieNode("cw")}),
    "ċ": TrieNode("ċ", {"ċ": TrieNode("ċċ"), "ġ": TrieNode("ċġ")}),
    "d": TrieNode("d", {"d": TrieNode("dd")}),
    "ð": TrieNode("ð", {"ð": TrieNode("ðð")}),
    "e": TrieNode("e", {"a": TrieNode("ea"), "o": TrieNode("eo")}),
    "ę": TrieNode("ę"),
    "ē": TrieNode("ē", {"a": TrieNode("ēa"), "o": TrieNode("ēo")}),
    "f": TrieNode("f", {"f": TrieNode("ff")}),
    "g": TrieNode("g", {"c": TrieNode("gc", {"g": TrieNode("gcg")}), "g": TrieNode("gg")}),
    "ġ": TrieNode("ġ", {"ġ": TrieNode("ġġ")}),
    "h": TrieNode("h", {"h": TrieNode("hh")}),
    "i": TrieNode("i", {"e": TrieNode("ie"), "o": TrieNode("io")}),
    "ī": TrieNode("ī", {"e": TrieNode("īe"), "o": TrieNode("īo")}),
    "k": TrieNode("k", {"k": TrieNode("kk")}),
    "l": TrieNode("l", {"l": TrieNode("ll")}),
    "m": TrieNode("m", {"m": TrieNode("mm")}),
    "n": TrieNode("n", {"n": TrieNode("nn")}),
    "o": TrieNode("o", {"e": TrieNode("oe")}),
    "ō": TrieNode("ō", {"e": TrieNode("ōe")}),
    "p": TrieNode("p", {"p": TrieNode("pp")}),
    "r": TrieNode("r", {"r": TrieNode("rr")}),
    "s": TrieNode("s", {"c": TrieNode("sc"), "ċ": TrieNode("sċ"), "s": TrieNode("ss")}),
    "t": TrieNode("t", {"h": TrieNode("th"), "t": TrieNode("tt")}),
    "þ": TrieNode("þ", {"þ": TrieNode("þþ")}),
    "u": TrieNode("u", {"u": TrieNode("uu")}),
    "ū": TrieNode("ū"),
    "w": TrieNode("w", {"w": TrieNode("ww")}),
    "ƿ": TrieNode("ƿ", {"ƿ": TrieNode("ƿƿ")}),
    "x": TrieNode("x", {"x": TrieNode("xx")}),
    "y": TrieNode("y"),
    "ȳ": TrieNode("ȳ"),
    "z": TrieNode("z", {"z": TrieNode("zz")}),
}
def get_old_english_phonemes(word):
    graphs = get_graphs(word)
    return get_phonemes(graphs)

def get_graphs(word):
    graphs = []
    current_node = None

    for i in range(0, len(word)):
        char = word[i]

        if current_node != None:
            if char in current_node.children:
                print("- new char '" + str(char) + "'")
                current_node = current_node.children[char]
            else:
                print("- ending graph with '" + str(char) + "'")
                graphs.append(current_node.graph)
                current_node = None

        if current_node == None:
            if char in graph_trie:
                print("- new graph")
                current_node = graph_trie[char]
            else:
                print("ERROR: '" + str(char) + "' not in graph trie")

    if current_node != None:
        graphs.append(current_node.graph)

    return graphs

def get_phonemes(graphs):
    phonemes = []

    for i in range(0, len(graphs)):
        anteprev = None
        prev = None
        next = None

        if i > 0:
            prev = graphs[i-1]

        if i > 1:
            anteprev = graphs[i-2]
        if i < len(graphs) - 1:
            next = graphs[i+1]

        phonemes.append(get_phoneme(graphs[i], anteprev, prev, next))

    return phonemes

def get_phoneme(graph, anteprev_g, prev_g, next_g):
    if graph == "a":
        return "ɑ"
    elif graph == "ā":
        return "ɑː"
    elif graph == "æ":
        return "æ"
    elif graph == "ǣ":
        return "æː"
    elif graph == "b":
        return "b"
    elif graph == "bb":
        return "bː"
    elif graph == "c":
        # need to handle intervening ns
        if next_g and next_g[0] in front_vowels:
            return "tʃ"
        if prev_g and prev_g[-1] in front_vowels and not (next_g and next_g[0] in back_vowels):
            return "tʃ"
        if prev_g and prev_g[-1] == "n" and anteprev_g and anteprev_g[-1] in front_vowels and not (next_g and next_g[0] in back_vowels):
            return "tʃ"
        else:
            return "k"
    elif graph == "cc":
        return "kk"
    elif graph == "ċ":
        return "tʃ"
    elif graph in ["cg", "gc", "cgg", "ccg", "gcg", "ċġ", "ġċ"]:
        # sometimes, unpredictably /ɣ/ + /ɣɣ/
        if prev_g == "n":
            return "j"
        else:
            return "jj"
    elif graph == "d":
        return "d"
    elif graph == "dd":
        return "dd"
    elif graph == "ð":
        return "θ"
    elif graph == "ðð":
        return "θθ"
    if graph == "e":
        return "e"
    elif graph == "ē":
        return "eː"
    if graph == "æ":
        return "æ"
    elif graph == "ǣ":
        return "æː"
    elif graph == "ea":
        # Some say it's /ɑ/ after a palatal c or g
        # Wiki has /æɑ̯/, dropped the diacritic
        return "æɑ"
    elif graph == "ēa":
        # Dropped diacritic as above
        return "æːɑ"
    elif graph == "eo":
        return "eo"
    elif graph == "ēo":
        return "eːo"
    elif graph == "f":
        return "f"
    elif graph == "g":
        if next_g and next_g[0] in front_vowels:
            return "j"
        if prev_g and prev_g[-1] in front_vowels and not (next_g and next_g[0] in back_vowels):
            return "j"
        else:
            return "ɣ"
    elif graph == "gg":
        return "ɣɣ"
    elif graph == "ġ":
        return "j"
    elif graph == "h":
        return "x"
    elif graph == "i":
        return "i"
    elif graph == "ī":
        return "iː"
    elif graph == "ie":
        return "iy"
    elif graph == "īe":
        return "iːy"
    elif graph == "io":
        return "io"
    elif graph == "īo":
        return "iːo"
    elif graph == "k":
        return "k"
    elif graph == "kk":
        return "kk"
    elif graph == "l":
        return "l"
    elif graph == "ll":
        return "ll"
    elif graph == "m":
        return "m"
    elif graph == "mm":
        return "mm"
    elif graph == "n":
        return "n"
    elif graph == "nn":
        return "nn"
    elif graph == "o":
        return "o"
    elif graph == "ō":
        return "oː"
    elif graph == "oe":
        return "ø"
    elif graph == "ōe":
        return "øː"
    elif graph == "p":
        return "p"
    elif graph == "pp":
        return "pp"
    elif graph == "cw":
        return "kw"
    elif graph == "r":
        return "r"
    elif graph == "rr":
        return "rr"
    elif graph == "s":
        return "s"
    elif graph == "ss":
        return "ss"
    elif graph == "sc" or graph == "sċ":
        if prev_g in vowels and next_g in vowels:
            return "ʃʃ"
        else:
            return "ʃ"
    elif graph == "t":
        return "t"
    elif graph == "tt":
        return "tt"
    elif graph == "th":
        return "θ"
    elif graph == "þ":
        return "θ"
    elif graph == "þþ":
        return "θθ"
    elif graph == "u":
        return "u"
    elif graph == "ū":
        return "uː"
    elif graph == "uu":
        return "w"
    elif graph == "ƿ":
        return "w"
    elif graph == "w":
        return "w"
    elif graph == "x":
        return "ks"
    elif graph == "y":
        return "y"
    elif graph == "ȳ":
        return "yː"
    elif graph == "z":
        return "ts"

    return "?"
