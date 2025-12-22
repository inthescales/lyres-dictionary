from forms.formset import FormSet

class LatinVerbFormSet(FormSet):
    def __init__(self, present: str, infinitive: str, perfect: str, supine: str):
        self.present = present
        self.infinitive = infinitive
        self.perfect = perfect
        self.supine = supine
