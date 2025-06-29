from src.tools.morphs.schemas.properties import properties as valid_properties
from src.tools.morphs.schemas.tags import tags as valid_tags
from src.tools.morphs.schemas.types import morph_types as valid_types

# Type Representations =================================

# Representations of data types that appear in the morph files, to be used validating
# types and allowed values

class Type:
    def is_valid(self, value, meta):
        return self.get_errors(value, meta)

    def __str__(self):
        return "Type(" + str(self.value) + ")"

class Primitive(Type):
    name = "generic primitive"

    def __init__(self, type, valueset=None):
        self.type = type
        self.valueset = valueset

    def __str__(self):
        if self.valueset != None:
            return "Primitive(" + str(self.valueset.name) + ")"
        else:
            return "Primitive()"

    def get_errors(self, value, meta):
        errors = []

        if type(value) != self.type:
            errors.append(TypeError("invalid value '" + str(value) + "' " + meta.context + ". Expected type " + self.name))
        elif self.valueset != None and value not in self.valueset.values:
            errors.append(TypeError("invalid " + self.valueset.name + " '" + str(value) + "' " + str(meta.context) + "."))

        return errors

class Bool(Primitive):
    name = "boolean"

    def __init__(self, valueset=None):
        Primitive.__init__(self, bool, valueset)

    def __str__(self):
        return "Bool()"

class Integer(Primitive):
    name = "integer"
    def __init__(self, valueset=None):
        Primitive.__init__(self, int, valueset)

    def __str__(self):
        if self.valueset != None:
            return "Integer(" + str(self.valueset.name) + ")"
        else:
            return "Integer()"

class String(Primitive):
    name = "string"

    def __init__(self, valueset=None):
        Primitive.__init__(self, str, valueset)

    def __str__(self):
        if self.valueset != None:
            return "String(" + self.valueset.name + ")"
        else:
            return "String()"

class Collection(Type):
    name = "generic collection"

    def __init__(self, subtype):
        self.subtype = subtype

    def __str__(self):
        return "Collection(" + str(self.subtype) + ")"

class Array(Collection):
    name = "list"

    def __init__(self, subtype, require_all=True):
        Collection.__init__(self, subtype)
        self.require_all = require_all

    def __str__(self):
        return "Array(" + str(self.subtype) + ")"

    def get_errors(self, value, meta):
        # Check that the value is a list
        if type(value) != list:
            return [TypeError("invalid value type " + meta.context + ". Expected type " + type_name(self))]

        child_meta = meta.new("in list " + meta.context)

        # If require_all is false, only check that at least one value matches
        if not self.require_all:
            if not any([len(self.subtype.get_errors(child, child_meta)) == 0 for child in value]):
                return [TypeError("list " + meta.context + " must contain an element of type " + type_name(self.subtype))]
            else:
                return []

        # Otherwise, check that all elements match
        errors = []
        for item in value:
            child_errors = self.subtype.get_errors(item, child_meta)
            if len(child_errors) > 0:
                if issubclass(type(self.subtype), Primitive):
                    errors.append(TypeError("invalid list member '" + str(item) + "' in list " + meta.context + ". List entries should be " + type_name(self.subtype, True) + "."))
                else:
                    errors += child_errors

        return errors

# May be a single value, or a list of values of the same type
class One_Or_More(Collection):
    name = "one-or-list"

    def __str__(self):
        return "One-Or-More(" + str(self.subtype) + ")"

    def get_errors(self, value, meta):
        if type(value) == list:
            return Array(self.subtype).get_errors(value, meta)
        
        errors = []
        child_errors = self.subtype.get_errors(value, meta)
        if len(child_errors) > 0 and issubclass(type(self.subtype), Primitive):
            errors.append(TypeError("invalid value '" + str(value) + "' " + meta.context + ". Expected type " + type_name(self)))
        else:
            errors += child_errors

        return errors

class Dict(Type):
    name = "dictionary"

    def __init__(self, reference, restrict=True):
        self.reference = reference
        self.restrict = restrict

    def __str__(self):
        return "Dict(" + str(self.reference) + ")"

    def key_match(self, value, meta):
        return type(value) == dict and all([type(exp) == Opt or key in value.keys() for key, exp in self.reference.items()])

    def get_errors(self, value, meta):
        errors = []

        # Check that value is a dictionary
        if type(value) != dict:
            return [TypeError("invalid value type " + meta.context + "'. Expected dictionary with reference key '" + str(self.reference) + "'")]

        # Check that all required keys are present
        missing_keys = [key for key, exp in self.reference.items() if type(exp) != Opt and key not in value.keys()]
        if len(missing_keys) > 0:
            for key in missing_keys:
                errors.append(TypeError("missing required key '" + str(key) + "' " + meta.missing_value_context))

        # If restricted, check that no keys outside the spec are present
        if self.restrict:
            extra_keys = [key for key in value.keys() if key not in self.reference.keys()]
            if len(extra_keys) > 0:
                errors.append(TypeError("unrecognized keys " + str(extra_keys) + " found in dictionary " + str(meta.context) + ""))

        # Check that values have the expected types
        for key, exp in self.reference.items():
            if key in value:
                child_meta = meta.new("for key '" + key + "' in dict '" + str(value) + "'")
                errors += exp.get_errors(value[key], child_meta)

        return errors

# Placeholder for another validation node that will be read at execution
# time from the list of schemata.
# Necessary to validate recursively nested data structures
class Schema(Type):
    def __init__(self, schema_key):
        self.schema_key = schema_key
        self.name = "schema with key '" + self.schema_key + "'"

    def __str__(self):
        return "Schema(" + str(self.schema_key) + ")"

    def get_errors(self, value, meta):
        # Check that the given schema key is valid
        if self.schema_key not in meta.schemata:
            return [TypeError("Unknown schema key '" + self.schema_key + "' in dictionary specification")]

        # Pass on child errors, or give a schema error if only weak errors are received.
        child_errors = meta.schemata[self.schema_key].get_errors(value, meta)
        if len(child_errors) > 0 and all([isinstance(err, WeakError) for err in child_errors]):
            return [TypeError("invalid value '" + str(value) + "' " + meta.context + ". Expected value of schema type '" + self.schema_key + "'")]
        else:
            return child_errors

# Represents a value that may be None or another type.
# Also used to represent optional keys in a Dict node.
class Opt(Type):
    name = "optional"

    def __init__(self, base_type):
        self.base_type = base_type

    def __str__(self):
        return "Opt(" + str(self.base_type) + ")"

    def get_errors(self, value, meta):
        if value == None:
            return []
        else:
            return self.base_type.get_errors(value, meta)

# Node where only one of a list of child nodes must succeed
class Any(Type):
    name = "any"

    def __init__(self, items, custom_error=None):
        self.items = items
        self.custom_error = custom_error

    def __str__(self):
        return "Any(" + str(self.items) + ")"

    def get_errors(self, value, meta):
        # If we have a key match, assume that that was the intended expansion
        for option in self.items:
            errors = option.get_errors(value, meta)

            if len(errors) == 0:
                return []
            elif type(option) == Dict and option.key_match(value, meta):
                return errors
            elif type(option) == Schema and option.schema_key in meta.schemata:
                schema_type = meta.schemata[option.schema_key]
                if type(schema_type) == Dict and schema_type.key_match(value, meta):
                    return errors

        if self.custom_error != None:
            return [TypeError(self.custom_error)]
        else:
            return [WeakError("no cases match in 'any' " + meta.context + ".")]

# Other Types ----------------------------

# Represents a list of acceptable values for a certain node.
class ValueSet:
    def __init__(self, name, values):
        self.name = name
        self.values = values

# Validation metadata
class Meta:
    def __init__(self, context, schemata, missing_value_context=None, context_override=False, ident=None):
        self.context = context
        self.missing_value_context = missing_value_context
        self.schemata = schemata
        self.context_override = context_override
        self.ident = ident

        if self.missing_value_context == None:
            self.missing_value_context = self.context

    def new(self, new_context):
        if self.context_override:
            return self
        else:
            return Meta(new_context, self.schemata, ident=self.ident)

# General error type for indicating type validation errors
class TypeError:
    def __init__(self, text):
        self.text = text

# A weak error indicates an error that isn't able to give much useful feedback,
# and may be pre-empted by parent nodes.
# Used by Any nodes when the code can't guess which case "should" have been valid.
class WeakError(TypeError):
    def __init__(self, text):
        TypeError.__init__(self, text)

# Schemata ===========================================

class ValueSets:
    prop = ValueSet("property", valid_properties)
    tag  = ValueSet("tag", valid_tags)
    type = ValueSet("type", valid_types)

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
