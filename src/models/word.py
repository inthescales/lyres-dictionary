from src.models.environment import Environment
from src.models.morph import Morph

class Word:
    
    def __init__(self, morphothec):
        self.morphs = []
        self.order_added = []
        self.morphothec = morphothec
    
    # Mutation -----------------------------------
    
    def set_keys(self, keys):
        self.set_morphs([Morph.with_key(key, self.morphothec) for key in keys])

    def set_morphs(self, morphs):
        self.morphs = morphs
        self.order_added = self.default_order(morphs)
        self.refresh_morphs()

    def add_prefix(self, morph):
        self.morphs = [morph] + self.morphs
        self.order_added.append(morph)
        self.refresh_morphs()
            
    def add_suffix(self, morph):
        self.morphs = self.morphs + [morph]
        self.order_added.append(morph)
        self.refresh_morphs()
        
    def add_affixes(self, prefix, suffix):
        self.morphs = [prefix] + self.morphs + [suffix]
        self.order_added += [prefix, suffix]
        self.refresh_morphs()

    def refresh_morphs(self):
        for i in range(0, len(self.morphs)):
            env = self.environment_for_index(i)
            self.morphs[i].refresh(env)

    # Public accessors -------------------------------

    def first_morph(self):
        if len(self.morphs) > 0:
            return self.morphs[0]
        else:
            return None
    
    def last_morph(self):
        if len(self.morphs) > 0:
            return self.morphs[len(self.morphs)-1]
        else:
            return None

    def root_morph(self):
        for morph in self.morphs:
            if morph.get_type() not in ["prep", "prefix", "suffix"]:
                return morph

    # Returns the environment of a potential prefix.
    def prefix_environment(self):
        return self.environment_for_index(-1)

    # Returns the environment of a potential suffix.
    def suffix_environment(self):
        return self.environment_for_index(len(self.morphs))
    
    def size(self):
        length = 0
        for morph in self.morphs:
            if not morph.has_tag("no-length"):
                length += 1
                
        return length
        
    def get_type(self):
        if self.first_morph().is_prefix() and "derive-to" in self.first_morph().morph and not self.last_morph().is_suffix():
            return self.first_morph().morph["derive-to"]

        return self.last_morph().get_type()

    def get_origin(self):
        return self.last_morph().morph["origin"]

    def get_keys(self):
        return [morph.morph["key"] for morph in self.morphs]

    # Whether this is a verb that specifies its own object
    def specifies_object(self):
        if self.get_type() != "verb":
            return False

        for morph in self.morphs:
            if morph.has_tag("object-specifier"):
                return True

        return False

    # Helpers --------------------------------------------

    def environment_for_index(self, index):
        anteprev_morph, prev_morph, next_morph, postnext_morph = (None, None, None, None)

        if index > 0:
            prev_morph = self.morphs[index - 1]
        if index > 1:
            anteprev_morph = self.morphs[index - 2]
        if index < len(self.morphs) - 1:
            next_morph = self.morphs[index + 1]
        if index < len(self.morphs) - 2:
            postnext_morph = self.morphs[index + 2]

        specifies_object = self.specifies_object()

        return Environment(anteprev_morph, prev_morph, next_morph, postnext_morph, specifies_object)

    # Returns the given morphs in a likely order of addition.
    # This represents the earlier logic, mostly applicable to Latin and Greek,
    # where morphs are assumed to be added in the order root > prefixes (in reverse order)
    # > suffixes (in order)
    #
    # Should only be used in testing
    def default_order(self, morphs):
        ordered = []
        prefix_stack = []

        for morph in self.morphs:
            if morph.is_prefix():
                prefix_stack.append(morph)
            else:
                ordered.append(morph)

                if len(prefix_stack) > 0 and morph.is_root():
                    for prefix in reversed(prefix_stack):
                        ordered.append(prefix)
                    prefix_stack = []

        return ordered
