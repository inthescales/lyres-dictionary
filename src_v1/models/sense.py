from src.tools.morphs.schemas.periods import default_period_for

class Sense:
    def __init__(self, sdict, language):
        self.dict = sdict

        if "period" in sdict:
            self.period = sdict["period"]
        else:
            self.period = default_period_for(language)
