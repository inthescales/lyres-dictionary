import re

from enum import Enum, auto
from typing import Optional

import lemminflect

class InflectionType(Enum):
    """A type of inflection that can be applied to a modern English word."""
    singular              = auto()
    plural                = auto()
    infinitive            = auto()
    third_person_singular = auto()
    present_participle    = auto()
    past_participle       = auto()

    @property
    def lemminflect_code(self) -> Optional[str]:
        """The code to sent to lemminflect to produce this type of inflection, or None if identical to the lemma"""
        match self:
            case InflectionType.singular:
                return "NN"
            case InflectionType.plural:
                return "NNS"
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

def inflect_bracketed(phrase: str, inflection_type: InflectionType) -> str:
    """Returns the phrase string with all bracketed substrings inflected in the specified way"""
    result = phrase

    def inflect_match(m: re.Match[str]) -> str:
        return inflect(m.group(1), inflection_type)

    return re.sub(r'\[(\w*)\]', inflect_match, result)

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
