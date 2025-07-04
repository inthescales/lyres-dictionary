import json

import src.tools.morphs.morphs_files as file_tool
import src.tools.morphs.sort_alphabetical as alphabetical
import src.tools.morphs.sort_numerical as numerical

from collections import OrderedDict

from src.utils.terminal import Color, color_text
from src.tools.morphs.schemas.properties import properties as properties_list
from src.tools.morphs.schemas.tags import tags as tags_list

indent_spaces = 4

# Get a number of spaces appropriate to the given indentation depth
def spaces(depth):
    return " " * depth * indent_spaces

# Sort given morphs alphabetically according to their keys
def sort(filename, morphs):
    if "number" in filename:
        return numerical.num_sorted(morphs)
    else:
        return alphabetical.key_sorted(morphs)

# Returns an ordered dict representing the morph, with its keys in schema-order
def ordered_morph(morph):
    ordered = OrderedDict()

    for prop in properties_list:
        if prop in morph:
            if prop == "tags":
                ordered[prop] = ordered_tags(morph["tags"])
            else:
                ordered[prop] = morph[prop]

    return ordered

# Returns a tags array with the tags sorted by schema-order
def ordered_tags(tags):
    ordered = []
    for tag in tags_list:
        if tag in tags:
            ordered.append(tag)

    return ordered

# Format a property given properties indicating its place in a morph structure
def format(obj, indent=0, tag_stack=[]):
    formatted = ""

    # Format a list
    if isinstance(obj, list):
        one_item = len(obj) == 1

        formatted += "["
        if not one_item:
            formatted += "\n"

        for index in range(0, len(obj)):
            element = obj[index]
            separate_line = (index < len(obj) - 1) and should_break_between(obj[index], obj[index + 1], tag_stack + [None])
            separated_last = (index > 0) and should_break_between(obj[index - 1], obj[index], tag_stack + [None])

            if not one_item and (index == 0 or separated_last):
                formatted += spaces(indent + 1)

            if should_format(element, None, tag_stack):
                added_indent = 0
                if not one_item:
                    added_indent = 1
                formatted += format(element, indent + added_indent, tag_stack + [None])
            else:
                formatted += unformatted(element)

            if index < len(obj) - 1:
                formatted += ","

            if not one_item and (index == len(obj) - 1 or separate_line):
                formatted += "\n"
            elif not one_item:
                formatted += " "

        if not one_item:
            formatted += spaces(indent)

        formatted += "]"

    # Format a dictionaryu
    elif isinstance(obj, dict):
        keys = list(obj.keys())
        should_indent = should_indent_dict(obj, tag_stack)

        formatted += "{"
        if should_indent:
            formatted += "\n"
        else:
            formatted += " "

        for index in range(0, len(keys)):
            key = keys[index]
            if should_indent:
                formatted += spaces(indent + 1)
            formatted += "\"" + key + "\": "

            if should_format(obj[key], key, tag_stack):
                added_indent = 0
                if should_indent:
                    added_indent = 1
                formatted += format(obj[key], indent + added_indent, tag_stack + [key])
            else:
                formatted += unformatted(obj[key])

            if index < len(obj) - 1:
                formatted += ","

            if should_indent:
                formatted += "\n"
            elif formatted[-1] not in ["]", "}"]:
                formatted += " "

        if should_indent:
            formatted += spaces(indent)

        formatted += "}"

    elif isinstance(obj, str):
        formatted += "\"" + obj + "\""

    elif isinstance(obj, int):
        formatted += str(obj)

    return formatted

# Get single-line dump of the given object
def unformatted(obj):
    dump = json.dumps(obj, ensure_ascii=False)
    dump = dump.replace("{", "{ ")
    dump = dump.replace("}", " }")
    return dump

# Whether there should be a newline after a comma separating the two elements in a list
def should_break_between(first, second, tag_stack):
    # Two dictionaries, both indented, not within a operator list
    if isinstance(first, dict) \
        and isinstance(second, dict) \
        and should_indent_dict(first, tag_stack) \
        and should_indent_dict(first, tag_stack) \
        and not (len(tag_stack) > 1 and tag_stack[-2] in ["and", "or"]):
        return False

    return True

# Returns whether the given dict should be separated from its container and indented
def should_indent_dict(element, tag_stack):
    keys = list(element.keys())

    # Don't indent 'not' if it's inside an 'and' or an 'or'
    if len(keys) == 1 and keys[0] in ["not", "and", "or"] \
        and len(tag_stack) > 1 and tag_stack[-2] in ["and", "or"]:
        return False

    return True

# Returns whether the given element should be formatted on multiple lines or condensed onto one
def should_format(element, key, tag_stack):
    stacksize = len(tag_stack)

    # Assimilation case lists
    if "form-assimilation" in tag_stack and "case" in tag_stack:
        return False

    # Lists in formsets
    if "form-oe" in tag_stack and type(element) == list:
        return False

    # Lists appearing in top-level morph keys
    if key:
        if key in [
            "derive-from",
            "suffixes",
            "tags"
        ] \
        or ( \
            key.startswith("form-") \
            and not key in ["form-assimilation", "form-oe"] \
        ) \
        or (key == "gloss" or key.startswith("gloss-")):
            return False

    # Elements within morph specifiers, except those listed in and/or statements
    if any([x in tag_stack for x in ["follows", "precedes"]]) \
        and not key in ["case", "and", "or"] \
        and not (isinstance(element, dict) and any([x in element for x in ["and", "or"]])) \
        and not (isinstance(element, dict) and "not" in element and any([x in element["not"] for x in ["and", "or"]])):
        return False

    return True

# Format the given morph files, with the given metadata and options
def format_morphs(files, test):
    changed = 0

    for file in files:
        # Read in morphs
        morphs = file_tool.get_morphs_from(file)

        # Sort morphs
        morphs = sort(file, morphs)

        # Order morph properties
        morphs = [ordered_morph(m) for m in morphs]

        # Format morphs
        with open(file, "r") as file_data:
            before = file_data.read()
        
        formatted = format(morphs)

        # Output
        if test:
            print(formatted)
        else:
            file_tool.write_formatted_to(formatted, file)

        if before != formatted:
            changed += 1

    if changed > 0:
        print(color_text(Color.yellow, str(changed) + " files changed"))
    else:
        print(color_text(Color.green, "0 files changed"))

    return changed
