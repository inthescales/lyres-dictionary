import src.tools.morphs.sort_alphabetical as alphabetical

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

# This array represents the desired numerical order for morph sorts.
# Items appearing first in this list will appear first in sort order.
# Items grouped in an array together have equal priority.
# Numbers not in this array will appear at the end in no particular order.
number_priority_list = [
    ["no", "none", "zero"],
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "hundred",
    "thousand",
    "million",
    "billion",
    "few",
    "many",
    ["too few", "insufficient"],
    ["too many", "excessive"],
    ["all", "every", "each"]
]

number_priority_map = generate_mapping(number_priority_list)

type_priority_list = [
    "noun",
    "adj",
    "prefix"
]

type_priority_map = generate_mapping(type_priority_list)

# Get the sort priority of the given morph
def get_priority(morph, mapping, type_mapping):
    if morph["type"] in type_priority_map:
        type_priority = type_priority_map[morph["type"]]
    else:
        type_priority = len(type_priority_list)

    number_priority = None
    for number, priority in number_priority_map.items():
        if number in morph["gloss"]:
            number_priority = priority

    if number_priority == None:
        number_priority = len(number_priority_list)

    return [type_priority, number_priority] + [alphabetical.get_sort_key(char) for char in morph["key"]]

# Returns the given morphs sorted in numerical sort
def num_sorted(morphs):
    return sorted(morphs, key=lambda morph: get_priority(morph, number_priority_map, type_priority_map))
