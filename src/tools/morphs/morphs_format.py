import json
import sys

from morphs_files import morphs_from

indent_spaces = 4

def spaces(depth):
    return " " * depth * indent_spaces

def sort(morphs):
    return sorted(morphs, key=lambda m: m["key"])

def format(obj, indent=0, tag_stack=[]):
    formatted = ""

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

def unformatted(obj):
    dump = json.dumps(obj)
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

def should_indent_dict(element, tag_stack):
    keys = list(element.keys())

    # Don't indent 'not' if it's inside an 'and' or an 'or'
    if len(keys) == 1 and keys[0] in ["not", "and", "or"] \
        and len(tag_stack) > 1 and tag_stack[-2] in ["and", "or"]:
        return False

    return True

def should_format(element, key, tag_stack):
    stacksize = len(tag_stack)

    # Children in assimilation specifiers
    if "form-assimilation" in tag_stack:
        return False

    # Lists appearing in top-level morph keys
    if key:
        if key in [
            "derive-from",
            "prefix-on",
            "suffixes",
            "tags"
        ] \
        or ( \
            key.startswith("form-") \
            and not key == "form-assimilation" \
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

# Prints the sorted and formatted contents of a single specified file
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("ERROR: morph format must take one file argument")
        sys.exit(0)

    file = sys.argv[1]
    morphs = morphs_from(file)
    formatted = format(morphs)

    print(formatted)
