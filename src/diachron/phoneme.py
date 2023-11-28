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

    def is_vowel(self):
        for char in ["a", "ɑ", "æ", "e", "ɛ", "i", "o", "u", "y", "ə"]:
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
        return self.value in ["b", "d", "g", "m", "n", "l", "r", "w", "dʒ"]

    def is_short(self):
        return not "ː" in self.value

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
