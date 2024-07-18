from src.evolutor.engine.phoneme import Phoneme

import src.evolutor.language.oe_orthography as orth

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
    "s": TrieNode("s", {"ċ": TrieNode("sċ"), "s": TrieNode("ss")}),
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
    "'": TrieNode("'"),
    "|": TrieNode("|")
}

def to_phonemes(word):
    graphs = get_graphs(word)
    return get_phonemes(graphs)

def get_graphs(word):
    graphs = []
    current_node = None

    for i in range(0, len(word)):
        char = word[i].lower()

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
        if graph[0] in orth.vowels:
            new_polarity = "V"
        else:
            new_polarity = "C"

        if new_polarity == "V" and polarity != new_polarity:
            count += 1

    return count

def get_phonemes(graphs):
    phonemes = []
    stress_count = 0 # 0: unstressed, 1: next vowel will be stressed, 2: vowel is stressed
    inflectional = False

    if count_syllables(graphs) == 1 or "'" not in graphs:
        stress_count = 1

    for i in range(0, len(graphs)):
        if graphs[i] == "'":
            stress_count = 1
            continue

        if graphs[i] == "|":
            inflectional = True
            continue

        if graphs[i] == ".":
            continue
        
        if graphs[i] in (orth.consonants + orth.geminates):
            if stress_count == 2:
                stress_count = 0

        if graphs[i] in orth.vowels:
            if stress_count == 1:
                stress_count = 2

        anteprev = None
        prev = None
        next = None

        if i > 0:
            prev = graphs[i-1]
        if i > 1:
            anteprev = graphs[i-2]
        if i < len(graphs) - 1:
            next = graphs[i+1]

        is_stressed = stress_count == 2
        phonemes.append(get_phoneme(graphs[i], anteprev, prev, next, is_stressed, inflectional))

    return phonemes

def get_phoneme(graph, anteprev_g, prev_g, next_g, stressed, inflectional):
    if graph == "a":
        return Phoneme("a", stressed, inflectional)
    elif graph == "ā":
        return Phoneme("aː", stressed, inflectional)
    elif graph == "æ":
        return Phoneme("æ", stressed, inflectional)
    elif graph == "ǣ":
        return Phoneme("æː", stressed, inflectional)
    elif graph == "b":
        return Phoneme("b", False, inflectional)
    elif graph == "bb":
        return Phoneme("bb", False, inflectional)
    elif graph == "c":
        # Interpret all unmarked 'c's as non-palatalized
        return Phoneme("k", False, inflectional)
    elif graph == "cc":
        return Phoneme("kk", False, inflectional)
    elif graph == "ċ":
        return Phoneme("tʃ", False, inflectional)
    elif graph == "ċċ":
        return Phoneme("tʃtʃ", False, inflectional)
    elif graph in ["cg", "gc", "cgg", "ccg", "gcg", "ċġ", "ġċ"]:
        # These are sometimes represented as /j/ or /jj/, but for simplicity I use /dʒ/ in all cases
        return Phoneme("dʒ", False, inflectional)
    elif graph == "d":
        return Phoneme("d", False, inflectional)
    elif graph == "dd":
        return Phoneme("dd", False, inflectional)
    elif graph == "ð":
        return Phoneme("θ", False, inflectional)
    elif graph == "ðð":
        return Phoneme("θθ", False, inflectional)
    if graph == "e":
        return Phoneme("e", stressed, inflectional)
    elif graph == "ē":
        return Phoneme("eː", stressed, inflectional)
    if graph == "æ":
        return Phoneme("æ", stressed, inflectional)
    elif graph == "ǣ":
        return Phoneme("æː", stressed, inflectional)
    elif graph == "ea":
        # Wikipedia indicates /æa̯/, or /a/ after a palatal c or g
        # Using /ea/ for simplicity
        return Phoneme("ea", stressed, inflectional)
    elif graph == "ēa":
        # Simplified representation as above
        return Phoneme("eːa", stressed, inflectional)
    elif graph == "eo":
        return Phoneme("eo", stressed, inflectional)
    elif graph == "ēo":
        return Phoneme("eːo", stressed, inflectional)
    elif graph == "f":
        return Phoneme("f", False, inflectional)
    elif graph == "g":
        # Assuming all unmarked 'g's to be non-palatal
        return Phoneme("ɣ", False, inflectional)
    elif graph == "gg":
        return Phoneme("ɣɣ", False, inflectional)
    elif graph == "ġ":
        return Phoneme("j", False, inflectional)
    elif graph == "h":
        return Phoneme("x", False, inflectional)
    elif graph == "hh":
        return Phoneme("xx", False, inflectional)
    elif graph == "i":
        return Phoneme("i", stressed, inflectional)
    elif graph == "ī":
        return Phoneme("iː", stressed, inflectional)
    elif graph == "ie":
        # This digraph only appears in WS, and merged into either 'i' in EWS or 'y' in LWS
        # Interpreting directly as 'y' for simplicity
        return Phoneme("y", stressed, inflectional)
    elif graph == "īe":
        # As above
        return Phoneme("yː", stressed, inflectional)
    elif graph == "io":
        return Phoneme("io", stressed, inflectional)
    elif graph == "īo":
        return Phoneme("iːo", stressed, inflectional)
    elif graph == "k":
        return Phoneme("k", False, inflectional)
    elif graph == "kk":
        return Phoneme("kk", False, inflectional)
    elif graph == "l":
        return Phoneme("l", False, inflectional)
    elif graph == "ll":
        return Phoneme("ll", False, inflectional)
    elif graph == "m":
        return Phoneme("m", False, inflectional)
    elif graph == "mm":
        return Phoneme("mm", False, inflectional)
    elif graph == "n":
        return Phoneme("n", False, inflectional)
    elif graph == "nn":
        return Phoneme("nn", False, inflectional)
    elif graph == "o":
        return Phoneme("o", stressed, inflectional)
    elif graph == "ō":
        return Phoneme("oː", stressed, inflectional)
    elif graph == "oe":
        return Phoneme("ø", stressed, inflectional)
    elif graph == "ōe":
        return Phoneme("øː", stressed, inflectional)
    elif graph == "p":
        return Phoneme("p", False, inflectional)
    elif graph == "pp":
        return Phoneme("pp", False, inflectional)
    elif graph == "cw":
        return Phoneme("kw", False, inflectional)
    elif graph == "r":
        return Phoneme("r", False, inflectional)
    elif graph == "rr":
        return Phoneme("rr", False, inflectional)
    elif graph == "s":
        return Phoneme("s", False, inflectional)
    elif graph == "ss":
        return Phoneme("ss", False, inflectional)
    elif graph == "sc" or graph == "sċ":
        if prev_g in orth.vowels and next_g in orth.vowels:
            return Phoneme("ʃʃ", False, inflectional)
        else:
            return Phoneme("ʃ", False, inflectional)
    elif graph == "t":
        return Phoneme("t", False, inflectional)
    elif graph == "tt":
        return Phoneme("tt", False, inflectional)
    elif graph == "th":
        return Phoneme("θ", False, inflectional)
    elif graph == "þ":
        return Phoneme("θ", False, inflectional)
    elif graph == "þþ":
        return Phoneme("θθ", False, inflectional)
    elif graph == "u":
        return Phoneme("u", stressed, inflectional)
    elif graph == "ū":
        return Phoneme("uː", stressed, inflectional)
    elif graph == "uu":
        return Phoneme("w", False, inflectional)
    elif graph == "ƿ":
        return Phoneme("w", False, inflectional)
    elif graph == "w":
        return Phoneme("w", False, inflectional)
    elif graph == "x":
        return Phoneme("ks", False, inflectional)
    elif graph == "y":
        return Phoneme("y", stressed, inflectional)
    elif graph == "ȳ":
        return Phoneme("yː", stressed, inflectional)
    elif graph == "z":
        return Phoneme("ts", False, inflectional)

    return Phoneme("?", stressed, inflectional)
