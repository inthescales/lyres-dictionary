from src.expressions import evaluate_expression
from src.morphothec import Morphothec

class Word:
    
    def __init__(self, morphothec):
        self.morphs = []
        self.morphothec = morphothec
        
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
    
    # Modifying --------------------------------
    
    def set_keys(self, keys):
        
        self.morphs = []
        
        for key in keys:
            self.morphs.append( Morph(key, self.morphothec) )
            
        for i in range(0, len(self.morphs)-1):
            self.morphs[i].join(self.morphs[i+1])

    def add_prefix(self, morph):
        morph.join(self.first_morph())
        self.morphs = [morph] + self.morphs
            
    def add_suffix(self, morph):
        self.last_morph().join(morph)
        self.morphs = self.morphs + [morph]
        
    def add_affixes(self, prefix, suffix):
        self.add_prefix(prefix)
        self.add_suffix(suffix)
