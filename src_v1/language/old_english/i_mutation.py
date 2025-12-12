import src.language.old_english.orthography as orth

from src.evolutor.engine.phoneme import Phoneme
from src.evolutor.engine.transform_rig import Rig

def i_mutation(state):
    if state.current.is_vowel() and state.syllable_data.following_syllable_count == 0:
        precedes_nasal = state.next and state.next.value in ["m", "n"]
        return [i_mutate_phoneme(state.current, precedes_nasal, "mercian")]

def i_mutate_phoneme(phoneme, precedes_nasal, dialect):
    ws_pairs = {
        "a": "æ", "æ": "e", "e": "i", "o": "e", "u": "y",
        "ea": "y", "eo": "eo", "io": "y"
    }

    anglian_pairs = {
        "a": "æ", "æ": "e", "e": "i", "o": "e", "u": "y",
        "ea": "e", "eo": "eo", "io": "eo"
    }

    kentish_pairs = {
        "a": "e", "æ": "e", "e": "i", "o": "e", "u": "e",
        "ea": "e", "eo": "eo", "io": "eo"
    }

    if dialect == "west-saxon":
        pairs = ws_pairs
    elif dialect in ["mercian", "northumbrian"]:
        pairs = anglian_pairs
    elif dialect == "kentish":
        pairs = kentish_pairs

    is_long = phoneme.is_long()
    base_value = phoneme.get_shortened().value

    if base_value == "a" and precedes_nasal:
        new_value = "e"
    elif base_value in pairs:
        new_value = pairs[base_value]
    else:
        new_value = base_value

    new_phoneme = Phoneme(new_value, template=phoneme)
    if is_long:
        new_phoneme = new_phoneme.get_lengthened()

    return new_phoneme

def i_mutate_graph(graph, precedes_nasal, dialect):
    ws_pairs = {
        "a": "æ", "æ": "e", "e": "i", "o": "e", "u": "y",
        "ea": "y", "eo": "eo", "io": "y"
    }

    anglian_pairs = {
        "a": "æ", "æ": "e", "e": "i", "o": "e", "u": "y",
        "ea": "e", "eo": "eo", "io": "eo"
    }

    kentish_pairs = {
        "a": "e", "æ": "e", "e": "i", "o": "e", "u": "e",
        "ea": "e", "eo": "eo", "io": "eo"
    }

    if dialect == "west-saxon":
        pairs = ws_pairs
    elif dialect in ["mercian", "northumbrian"]:
        pairs = anglian_pairs
    elif dialect == "kentish":
        pairs = kentish_pairs

    is_long = False
    if graph in orth.long_vowels:
        is_long = True
        graph = orth.short_vowels[orth.long_vowels.index(graph)]

    if graph == "a" and precedes_nasal:
        new_graph = "e"
    elif graph in pairs:
        new_graph = pairs[graph]
    else:
        new_graph = graph

    if is_long:
        index = orth.short_vowels.index(new_graph)
        new_graph = orth.long_vowels[index]

    return new_graph

def get_i_mutated(phonemes, config):
    rig = Rig(phonemes)
    rig.run_capture(i_mutation, 1, "i-mutation", config)
    return rig.phonemes

def get_i_mutated_word(word, dialect):
    def get_last_vowel_cluster_indices():
        indices = []
        for i in reversed(range(0, len(word))):
            char = word[i]
            if char not in orth.vowels:
                if indices == []:
                    continue
                else:
                    return [i + 1] + indices
            elif char in orth.vowels:
                if indices == []:
                    indices = [i]

        if len(indices) == 1:
            indices = [0] + indices

        return cluster

    indices = get_last_vowel_cluster_indices()
    if len(indices) > 2:
        return word

    precedes_nasal = len(word) > indices[1] and word[indices[1] + 1] in ["m", "n"]
    old_vowels = word[indices[0]:indices[1] + 1]
    new_vowels = i_mutate_graph(old_vowels, precedes_nasal, dialect)

    return word[:indices[0]] + new_vowels + word[indices[1] + 1:]
