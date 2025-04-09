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

type_priority_list = [
    "noun",
    "adj",
    "prefix"
]

type_priority_map = generate_mapping(type_priority_list)

tag_priority_list = [
    "cardinal",
    "ordinal",
    "distributive",
    "multiplicative",
    "proportional"
]

tag_priority_map = generate_mapping(tag_priority_list)

# This array represents the desired numerical order for morph sorts.
# Items appearing first in this list will appear first in sort order.
# Items grouped in an array together have equal priority.
# Numbers not in this array will appear at the end in no particular order.
number_priority_list = [
    ["no", "none", "zero"],
    ["one", "first"],
    ["two", "second"],
    ["three", "third"],
    ["four", "fourth"],
    ["five", "fifth"],
    ["six", "sixth"],
    ["seven", "seventh"],
    ["eight", "eighth"],
    ["nine", "ninth"],
    ["ten", "tenth"],
    ["eleven", "eleventh"],
    ["twelve", "twelfth"],
    ["hundred", "hundredth"],
    ["thousand", "thousandth"],
    "few",
    "multiple",
    "many",
    ["too few", "insufficient"],
    ["too many", "excessive"],
    ["all", "every", "each"]
]

number_priority_map = generate_mapping(number_priority_list)

# Get the sort priority of the given morph
def get_priority(morph, mapping, type_mapping):
    if morph["type"] in type_priority_map:
        type_priority = type_priority_map[morph["type"]]
    else:
        type_priority = len(type_priority_list)

    tag_priority = len(tag_priority_list)
    if "tags" in morph:
        for tag in morph["tags"]:
            if tag in tag_priority_map:
                tag_priority = tag_priority_map[tag]
                break

    number_priority = len(number_priority_list)
    for number, priority in number_priority_map.items():
        if number in morph["gloss"]:
            number_priority = priority

    return [type_priority, tag_priority, number_priority] + [alphabetical.get_sort_key(char) for char in morph["key"]]

# Returns the given morphs sorted in numerical sort
def num_sorted(morphs):
    return sorted(morphs, key=lambda morph: get_priority(morph, number_priority_map, type_priority_map))
