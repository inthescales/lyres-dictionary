# TODO: Handle prefixes like 'ā-', 'ġe-' by essentially moving them to end of sort order

# Turns the priority array into a dictionary that can be queried during sort.
def generate_mapping(array):
    mapping = {}

    priority = 0
    for item in array:
        if isinstance(item, list):
            for subitem in item:
                mapping[subitem] = priority
        else:
            mapping[item] = priority

        priority += 1

    return mapping

# This array represents the desired alphabetical order for morph sorts.
# Items appearing first in this list will appear first in sort order.
# Items grouped in an array together have equal priority.
# Characters not in this array will appear at the end in no particular order.
priority_list = [
    "-",
    ["æ", "ǣ"],
    ["a", "ā"],
    "b",
    ["c", "ċ"],
    "d",
    ["e", "ē"],
    "f",
    ["g", "ġ"],
    "h",
    ["i", "ī"],
    "j",
    "k",
    "l",
    "m",
    "n",
    ["o", "ō"],
    "p",
    "q",
    "r",
    "s",
    "t",
    ["þ", "ð"],
    ["u", "ū"],
    "v",
    "w",
    "x",
    ["y", "ȳ"],
    "z",
    "|"
]

priority_map = generate_mapping(priority_list)

# Get the sort priority of the given character
def get_priority(char, mapping):
    if char in mapping:
        return mapping[char]
    else:
        return len(priority_list)

# Returns the given morphs sorted by key
def key_sorted(morphs):
    return sorted(morphs, key=lambda morph: [get_priority(char, priority_map) for char in morph["key"]])
