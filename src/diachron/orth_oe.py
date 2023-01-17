from src.diachron.phoneme import Phoneme

consonants = ["b", "c", "ċ", "cg", "d", "ð", "f", "g", "ġ", "h", "k", "l", "m", "n", "p", "cw", "r", "s", "sc", "t", "th", "þ", "uu", "w", "ƿ", "x", "z"]
vowels = ["a", "ā", "æ", "ǣ", "e", "ę", "ē", "ea", "ēa", "eo", "ēo", "i", "ī", "ie", "īe", "io", "īo", "o", "ō", "oe", "ōe", "u", "ū", "y", "ȳ"]
special_characters = ["'"]

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
    "'": TrieNode("'")
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
                current_node = current_node.children[char]
            else:
                graphs.append(current_node.graph)
                current_node = None

        if current_node == None:
            if char in graph_trie:
                current_node = graph_trie[char]

    if current_node != None:
        graphs.append(current_node.graph)

    return graphs

def count_syllables(graphs):
    count = 0
    polarity = None

    for graph in graphs:
        new_polarity = None
        if graph[0] in vowels:
            new_polarity = "vowel"
        else:
            new_polarity = "consonant"

        if new_polarity == "vowel" and polarity != new_polarity:
            count += 1

    return count

def get_phonemes(graphs):
    phonemes = []
    stressed = 0 # 0: unstressed, 1: next vowel will be stressed, 2: vowel is stressed

    if count_syllables(graphs) == 1 or "'" not in graphs:
        stressed = 1

    for i in range(0, len(graphs)):
        if graphs[i] == "'":
            stressed = 1
            continue

        if graphs[i] in consonants:
            if stressed == 2:
                stressed = 0

        if graphs[i] in vowels:
            if stressed == 1:
                stressed = 2

        anteprev = None
        prev = None
        next = None

        if i > 0:
            prev = graphs[i-1]
        if i > 1:
            anteprev = graphs[i-2]
        if i < len(graphs) - 1:
            next = graphs[i+1]

        phonemes.append(get_phoneme(graphs[i], anteprev, prev, next, stressed == 2))

    return phonemes

def get_phoneme(graph, anteprev_g, prev_g, next_g, stressed):
    if graph == "a":
        return Phoneme("ɑ", stressed)
    elif graph == "ā":
        return Phoneme("ɑː", stressed)
    elif graph == "æ":
        return Phoneme("æ", stressed)
    elif graph == "ǣ":
        return Phoneme("æː", stressed)
    elif graph == "b":
        return Phoneme("b")
    elif graph == "bb":
        return Phoneme("bː")
    elif graph == "c":
        # need to handle intervening ns
        if next_g and next_g[0] in front_vowels:
            return Phoneme("tʃ")
        if prev_g and prev_g[-1] in front_vowels and not (next_g and next_g[0] in back_vowels):
            return Phoneme("tʃ")
        if prev_g and prev_g[-1] == "n" and anteprev_g and anteprev_g[-1] in front_vowels and not (next_g and next_g[0] in back_vowels):
            return Phoneme("tʃ")
        else:
            return Phoneme("k")
    elif graph == "cc":
        return Phoneme("kk")
    elif graph == "ċ":
        return Phoneme("tʃ")
    elif graph in ["cg", "gc", "cgg", "ccg", "gcg", "ċġ", "ġċ"]:
        # sometimes, unpredictably /ɣ/ + /ɣɣ/
        if prev_g == "n":
            return Phoneme("j")
        else:
            return Phoneme("jj")
    elif graph == "d":
        return Phoneme("d")
    elif graph == "dd":
        return Phoneme("dd")
    elif graph == "ð":
        return Phoneme("θ")
    elif graph == "ðð":
        return Phoneme("θθ")
    if graph == "e":
        return Phoneme("e", stressed)
    elif graph == "ē":
        return Phoneme("eː", stressed)
    if graph == "æ":
        return Phoneme("æ", stressed)
    elif graph == "ǣ":
        return Phoneme("æː", stressed)
    elif graph == "ea":
        # Some say it's /ɑ/ after a palatal c or g
        # Wiki has /æɑ̯/, dropped the diacritic
        return Phoneme("æɑ", stressed)
    elif graph == "ēa":
        # Dropped diacritic as above
        return Phoneme("æːɑ", stressed)
    elif graph == "eo":
        return Phoneme("eo", stressed)
    elif graph == "ēo":
        return Phoneme("eːo", stressed)
    elif graph == "f":
        return Phoneme("f")
    elif graph == "g":
        if next_g and next_g[0] in front_vowels:
            return Phoneme("j")
        if prev_g and prev_g[-1] in front_vowels and not (next_g and next_g[0] in back_vowels):
            return Phoneme("j")
        else:
            return Phoneme("ɣ")
    elif graph == "gg":
        return Phoneme("ɣɣ")
    elif graph == "ġ":
        return Phoneme("j")
    elif graph == "h":
        return Phoneme("x")
    elif graph == "i":
        return Phoneme("i", stressed)
    elif graph == "ī":
        return Phoneme("iː", stressed)
    elif graph == "ie":
        return Phoneme("iy", stressed)
    elif graph == "īe":
        return Phoneme("iːy", stressed)
    elif graph == "io":
        return Phoneme("io", stressed)
    elif graph == "īo":
        return Phoneme("iːo", stressed)
    elif graph == "k":
        return Phoneme("k")
    elif graph == "kk":
        return Phoneme("kk")
    elif graph == "l":
        return Phoneme("l")
    elif graph == "ll":
        return Phoneme("ll")
    elif graph == "m":
        return Phoneme("m")
    elif graph == "mm":
        return Phoneme("mm")
    elif graph == "n":
        return Phoneme("n")
    elif graph == "nn":
        return Phoneme("nn")
    elif graph == "o":
        return Phoneme("o", stressed)
    elif graph == "ō":
        return Phoneme("oː", stressed)
    elif graph == "oe":
        return Phoneme("ø", stressed)
    elif graph == "ōe":
        return Phoneme("øː", stressed)
    elif graph == "p":
        return Phoneme("p")
    elif graph == "pp":
        return Phoneme("pp")
    elif graph == "cw":
        return Phoneme("kw")
    elif graph == "r":
        return Phoneme("r")
    elif graph == "rr":
        return Phoneme("rr")
    elif graph == "s":
        return Phoneme("s")
    elif graph == "ss":
        return Phoneme("ss")
    elif graph == "sc" or graph == "sċ":
        if prev_g in vowels and next_g in vowels:
            return Phoneme("ʃʃ")
        else:
            return Phoneme("ʃ")
    elif graph == "t":
        return Phoneme("t")
    elif graph == "tt":
        return Phoneme("tt")
    elif graph == "th":
        return Phoneme("θ")
    elif graph == "þ":
        return Phoneme("θ")
    elif graph == "þþ":
        return Phoneme("θθ")
    elif graph == "u":
        return Phoneme("u", stressed)
    elif graph == "ū":
        return Phoneme("uː", stressed)
    elif graph == "uu":
        return Phoneme("w")
    elif graph == "ƿ":
        return Phoneme("w")
    elif graph == "w":
        return Phoneme("w")
    elif graph == "x":
        return Phoneme("ks")
    elif graph == "y":
        return Phoneme("y", stressed)
    elif graph == "ȳ":
        return Phoneme("yː", stressed)
    elif graph == "z":
        return Phoneme("ts")

    return Phoneme("?", stressed)
