from src.expressions import evaluate_expression
from src.morphothec import Morphothec
from src.models.environment import Environment
from src.models.morph import Morph

class Word:
    
    def __init__(self, morphothec):
        self.morphs = []
        self.morphothec = morphothec
    
    # Mutation
    
    def set_keys(self, keys):
        self.morphs = [Morph(key, self.morphothec) for key in keys]
        self.refresh_morphs()

    def add_prefix(self, morph):
        self.morphs = [morph] + self.morphs
        self.refresh_morphs()
            
    def add_suffix(self, morph):
        self.morphs = self.morphs + [morph]
        self.refresh_morphs()
        
    def add_affixes(self, prefix, suffix):
        self.morphs = [prefix] + self.morphs + [suffix]
        self.refresh_morphs()

    def refresh_morphs(self):
        for i in range(0, len(self.morphs)):
            env = self.environment_for_index(i)
            self.morphs[i].refresh(env)

    # Public accessors

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
        return self.last_morph().get_type()

    def get_origin(self):
        return self.last_morph().morph["origin"]

    # Helpers

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


        return Environment(anteprev_morph, prev_morph, next_morph, postnext_morph)
