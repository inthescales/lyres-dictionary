from enum import StrEnum
from typing import Optional

import lemminflect

class InflectionType(StrEnum):
    """A type of inflection that can be applied to a modern English word."""
    singular              = "sg"
    plural                = "pl"
    adjective             = "adj"
    infinitive            = "inf"
    third_person_singular = "3sg"
    present_participle    = "part"
    past_participle       = "ppart"

    @property
    def lemminflect_code(self) -> Optional[str]:
        """The code to sent to lemminflect to produce this type of inflection, or None if identical to the lemma"""
        match self:
            case InflectionType.singular:
                return "NN"
            case InflectionType.plural:
                return "NNS"
            case InflectionType.adjective:
                return "JJ"
            case InflectionType.infinitive:
                return None
            case InflectionType.third_person_singular:
                return "VBZ"
            case InflectionType.present_participle:
                return "VBG"
            case InflectionType.past_participle:
                return "VBN"

# Returns an inflected form of the given word according to the mode
def inflect(word: str, inflection_type: InflectionType) -> str:
    """Returns an inflected form of the word, inflected according to the given type."""
    override_form = override_inflection(word, inflection_type)
    if override_form is not None:
        return override_form

    code = inflection_type.lemminflect_code
    if code is not None:
        return lemminflect.getInflection(word, tag=code)[0]
    else:
        return word

# Custom overrides for words the inflection library gets wrong
def override_inflection(word, inflection_type: InflectionType) -> Optional[str]:
    overrides: dict[str, dict[InflectionType, str]] = {
        "arms": {
            InflectionType.plural: "arms"
        },
        "die": {
            InflectionType.plural: "dice"
        },
        "do": {
            InflectionType.third_person_singular: "does",
            InflectionType.past_participle: "done"
        },
        "dusk": {
            InflectionType.plural: "dusks"
        },
        "flour": {
            InflectionType.plural: "flours"
        },
        "omen": {
            InflectionType.plural: "omens"
        },
        "ox": {
            InflectionType.plural: "oxen"
        },
        "people": {
            InflectionType.plural: "peoples"
        },
        "spittle": {
            InflectionType.plural: "spittles"
        },
        "sting": {
            InflectionType.present_participle: "stinging"
        },
        "two": {
            InflectionType.plural: "twos"
        },
        "urine": {
            InflectionType.plural: "urines"
        }
    }

    if word in overrides and inflection_type in overrides[word]:
        return overrides[word][inflection_type]
    else:
        return None
