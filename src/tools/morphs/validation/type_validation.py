from src.tools.morphs.schemas.properties import properties as valid_properties
from src.tools.morphs.schemas.tags import tags as valid_tags
from src.tools.morphs.schemas.types import morph_types as valid_types

# Placeholder types =================================

# These represent different types of values that appear in the data files, which
# are used for both type and value validation.

class Type:
    def is_valid(self, value, meta):
        return self.get_errors(value, meta)

class Meta:
    def __init__(self, key, expression, schemata):
        self.key = key
        self.expression = expression
        self.schemata = schemata

class Primitive(Type):
    name = "generic primitive"

    def __init__(self, type, valueset=None):
        self.type = type
        self.valueset = valueset

    def get_errors(self, value, meta):
        if type(value) != self.type:
            return ["invalid value type for key '" + meta.key + "' in dict " + str(meta.expression) + ". Expected type " + self.name]
        elif self.valueset != None and value not in self.valueset.values:
            return ["invalid " + self.valueset.name + " '" + value + "' found in dict " + str(meta.expression) + "."]

        return []

class Bool(Primitive):
    name = "boolean"

    def __init__(self, valueset=None):
        Primitive.__init__(self, bool, valueset)

class Integer(Primitive):
    name = "integer"
    def __init__(self, valueset=None):
        Primitive.__init__(self, int, valueset)

class String(Primitive):
    name = "string"

    def __init__(self, valueset=None):
        Primitive.__init__(self, str, valueset)

class Collection(Type):
    name = "generic collection"

    def __init__(self, subtype):
        self.subtype = subtype

class Array(Collection):
    name = "list"

    def get_errors(self, value, meta):
        if type(value) != list:
            return ["invalid value type for key '" + meta.key + "' in dict '" + str(meta.expression) + "'. Expected type " + type_name(self)]

        errors = []
        for item in value:
            child_errors = self.subtype.get_errors(item, meta)
            if len(child_errors) > 0 and issubclass(type(self.subtype), Primitive):
                errors += ["invalid list member '" + str(item) + "' for key '" + meta.key + "' in dict '" + str(meta.expression) + "'. List entries should be " + type_name(self.subtype, True)]
            else:
                errors += child_errors

        return errors

# May be a single value, or a list of values
class one_or_more(Collection):
    name = "one-or-list"

    def get_errors(self, value, meta):
        if type(value) == list:
            return Array(self.subtype).get_errors(value, meta)
        
        errors = self.subtype.get_errors(value, meta)
        if len(errors) > 0 and issubclass(type(self.subtype), Primitive):
            errors = ["invalid value '" + str(value) + "' for key '" + meta.key + "' in dict '" + str(meta.expression) + "'. Expected type " + type_name(self)]

        return errors

class Dict(Type):
    name = "dictionary"

    def __init__(self, reference, restrict=True):
        self.reference = reference
        self.restrict = restrict

    def key_match(self, value, meta):
        return type(value) == dict and all([type(exp) == Opt or key in value.keys() for key, exp in self.reference.items()])

    def get_errors(self, value, meta):
        errors = []

        # Check that value is a dict
        if type(value) != dict:
            return ["invalid value type for key '" + meta.key + "' in dict '" + str(meta.expression) + "'. Expected dictionary with reference key '" + self.reference + "'"]

        # Check that all required keys are present
        missing_keys = [key for key, exp in self.reference.items() if type(exp) != Opt and key not in value.keys()]
        if len(missing_keys) > 0:
            errors += ["missing keys '" + str(missing_keys) + "' for dictionary in expression '" + str(meta.expression) + "'"]

        # If restricted, check that no keys outside the spec are present
        if self.restrict:
            extra_keys = [key for key in value.keys() if key not in self.reference.keys()]
            if len(extra_keys) > 0:
                errors += ["unrecognized keys " + str(extra_keys) + " found for dictionary '" + str(self.reference) + "' in expression '" + str(meta.expression) + "'"]

        # Check that values have the expected types
        for key, exp in self.reference.items():
            if key in value:
                new_meta = Meta(key, value, meta.schemata)
                errors += exp.get_errors(value[key], new_meta)

        return errors

class Schema(Type):
    def __init__(self, schema_key):
        self.schema_key = schema_key
        self.name = "schema with key '" + self.schema_key + "'"

    def get_errors(self, value, meta):
        if self.schema_key not in meta.schemata:
            return ["Unknown schema key '" + self.schema_key + "' in dictionary specification"]

        return meta.schemata[self.schema_key].get_errors(value, meta)

class Opt(Type):
    name = "optional"

    def __init__(self, base_type):
        self.base_type = base_type

    def get_errors(self, value, meta):
        if value == None:
            return []
        else:
            return self.base_type.get_errors(value, meta)

class Any(Type):
    name = "any"

    def __init__(self, items):
        self.items = items

    def get_errors(self, value, meta):
        # If we have a key match, assume that that was the intended expansion
        for option in self.items:
            if type(option) == Dict and option.key_match(value, meta):
                return option.get_errors(value, meta)

        return ["invalid value type for key '" + meta.key + "' in expression '" + str(meta.expression) + "'."]

class ValueSet:
    def __init__(self, name, values):
        self.name = name
        self.values = values

# Schemata ===========================================

valueset_prop = ValueSet("property", valid_properties)
valueset_tag  = ValueSet("tag", valid_tags)
valueset_type = ValueSet("type", valid_types)

                                      # ARGUMENT TYPE             EVALUATION RESULT
schemata = {
    "expression": Any([
        Dict({"or":                   Array(Schema("expression"))}),      # true if any expression in list evaluates true
        Dict({"and":                  Array(Schema("expression"))}),      # true if all expressions in list evaluate true
        Dict({"not":                  Schema("expression")}),             # true if the expression evaluates false
        Dict({"has-key":              one_or_more(String())}),          # true if the morph's key matches the given string, or is in the list
        Dict({"has-type":             one_or_more(String(valueset_type))}), # true if the morph's type is equal to the string, or is in the list
        Dict({"has-property":         String(valueset_prop)}),              # true if the morph contains a value for the given property
        Dict({"has-tag":              String(valueset_tag)}),               # true if the morph contains the given tag
        Dict({"has-all-tags":         Array(String(valueset_tag))}),        # true if the morph contains all of the given tags
        Dict({"has-any-tags":         Array(String(valueset_tag))}),        # true if the morph contains any of the given tags
        Dict({"has-prefix":           one_or_more(String())}),          # true if the morph's form begins with the given string, or any in a given list
        Dict({"has-suffix":           one_or_more(String())}),          # true if the morph's form ends with the given string, or any in a given list
        Dict({"has-suffix-template":  one_or_more(String())}),          # true if the morph's form's ending matches the given string template, or any in a given list
                                                                        #   - C: matches any consonant
                                                                        #   - V: matches any vowel
                                                                        #   - other characters match as literals
        Dict({"has-conjugation":      one_or_more(Integer())}),          # true if the morph has a conjugation equal to the given integer
        Dict({"has-declension":       one_or_more(Integer())}),          # true if the morph has a declension equal to the given integer
        Dict({"syllable-count":       Integer()}),                      # true if the morph
        Dict({"is-root":              Bool()}),                         # true if the morph's type is a root type
        Dict({"is-final":             Bool()}),                         # true if no morphs follow this morph
        Dict({"final-or-semifinal-l": Bool()})                          # true if there is an l in the last two syllables
    ])
}

# Validation helpers =============================

# Get a name for the given type suitable for printing in error messages
def type_name(expected, plural=False):
    name = expected.name
    if issubclass(type(expected), Primitive) and expected.valueset != None:
        name = "(" + expected.name +") " + expected.valueset.name

    if plural:
        name += "s"

    if issubclass(type(expected), Collection):
        name += " of " + type_name(expected.subtype, True)

    return name
