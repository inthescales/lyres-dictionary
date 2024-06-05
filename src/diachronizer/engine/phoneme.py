class Letter:
    def __init__(self, string):
        self.value = string

    def __eq__(self, other):
        return self.value == other.value

class Phoneme:
    def __init__(self, value, stressed=False, inflectional=False, template=None, history=None):
        self.value = value

        if template:
            self.history = template.history
        else:
            self.history = []
        if history:
            self.history += history

        if template:
            self.stressed = template.stressed
            self.inflectional = template.inflectional
        else:
            self.stressed = stressed
            self.inflectional = inflectional

    def __eq__(self, other):
        return other \
            and self.value == other.value \
            and self.stressed == other.stressed \
            and self.inflectional == other.inflectional

    # Properties

    def is_vowel(self):
        for char in ["a", "ɑ", "æ", "e", "ɛ", "i", "o", "ɔ", "u", "y", "ə"]:
            if char in self.value:
                return True
        return False

    def is_consonant(self):
        return not self.is_vowel()

    def is_front_vowel(self):
        for char in ["i", "e", "ɛ", "y", "ø", "œ"]:
            if char in self.value:
                return True
        return False

    def is_back_vowel(self):
        for char in ["u", "o", "ɔ"]:
            if char in self.value:
                return True
        return False

    def is_voiced(self):
        return self.value in ["b", "d", "g", "ɣ", "m", "n", "l", "r", "w", "dʒ", "v", "z", "ð"]

    def is_plosive(self):
        plosives = ["b", "c", "ċ", "dʒ", "d", "g", "k", "p", "t"]
        return self.value in plosives

    def is_fricative(self):
        return self.value in ["x", "f", "s", "ʃ", "θ", "ɣ", "v", "z", "ð"]

    def is_nasal(self):
        plosives = ["n", "m"]
        return self.value in plosives
        
    def is_semivowel(self):
        plosives = ["l", "r", "w", "j"]
        return self.value in plosives
    
    def is_short(self):
        return not "ː" in self.value and not self.is_diphthong()

    def is_long(self):
        return "ː" in self.value

    def is_diphthong(self):
        value_cleaned = self.value
        value_cleaned.replace("ː", "")
        return len(value_cleaned) > 1

    def is_geminate(self):
        length = len(self.value)
        return self.is_consonant() and length % 2 == 0 \
            and self.value[:int(length/2)] == self.value[int(length/2):]

    # Transformations

    def get_voiced(self):
        unvoiced = ["p", "t", "k", "x", "tʃ", "f", "s", "θ"]
        voiced = ["b", "d", "g", "ɣ", "dʒ", "v", "z", "ð"]

        index = unvoiced.index(self.value[0])
        if not self.is_geminate():
            return Phoneme(voiced[index], template=self)
        else:
            return Phoneme(voiced[index] + voiced[index], template=self)

    def get_shortened(self):
        return Phoneme(self.value.replace("ː", ""), template=self)

    def get_lengthened(self):
        if "ː" not in self.value:
            return Phoneme(self.value[0] + "ː" + self.value[1:], template=self)
        else:
            return self

    def get_geminate_reduced(self):
        length = len(self.value)
        if self.is_geminate():
            return Phoneme(self.value[:int(length/2)], template=self)
        else:
            return self
