from enum import StrEnum

class Countability(StrEnum):
    """Countability property of a noun"""
    countable       = "count"
    mass            = "mass"
    singleton       = "singleton"
    uncountable     = "uncountable"

    @property
    def pluralizable(self) -> bool:
        """Whether nouns with this countability are typically pluralized"""
        match self:
            case Countability.countable:
                return True
            case Countability.mass | Countability.singleton | Countability.uncountable:
                return False
