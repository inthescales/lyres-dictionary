import re

from enum import StrEnum
from typing import Optional

import utils.inflection as inflection
import utils.logging as log

from word_base.senses.countability import Countability
from word_base.senses.sense import Sense, NounSense

class InflectionCode(StrEnum):
    """String codes for applying inflection during gloss substitution"""
    passthrough        = "@"
    singular           = "sg"
    force_singular     = "!sg"
    plural             = "pl"
    force_plural       = "!pl"
    infinitive         = "inf"
    subject_agreement  = "subj-agr"
    present_participle = "part"
    past_participle    = "ppart"

class InflectionCodeException(Exception):
    """Exception raised when an unrecognized inflection code is encountered in a gloss"""
    def __init__(self, code: str):
        self.args = (["Unrecognized inflection code '" + code + "'"], code)

def substitute(wrapped_sense: Sense, gloss: str, wrapped: str) -> str:
    """
    Applies inflections to the wrapped morph's gloss text, indicated by '%([inflection-code]).
    Also applies determiners and particles as appropriate.
    '"""
    def apply_code(m: re.Match[str]) -> str:
        code_str: str = m.group(1)

        try:
            code = InflectionCode(code_str)
            prefix: str = ""
            inflection_type: Optional[inflection.InflectionType] = None
            countability: Countability = Countability.uncountable
            if isinstance(wrapped_sense, NounSense):
                countability = wrapped_sense.countability

            match code:
                case InflectionCode.passthrough:
                    pass
                case InflectionCode.singular:
                    inflection_type = inflection.InflectionType.singular

                    match countability:
                        case Countability.countable:
                            prefix = "a "
                        case Countability.singleton:
                            prefix = "the "
                        case Countability.mass | Countability.uncountable:
                            pass

                case InflectionCode.force_singular:
                    inflection_type = inflection.InflectionType.singular
                case InflectionCode.plural:
                    match countability:
                        case Countability.countable:
                            inflection_type = inflection.InflectionType.plural
                        case Countability.singleton:
                            inflection_type = inflection.InflectionType.singular
                            prefix = "the "
                        case Countability.mass | Countability.uncountable:
                            inflection_type = inflection.InflectionType.singular

                case InflectionCode.force_plural:
                    inflection_type = inflection.InflectionType.plural
                case InflectionCode.infinitive:
                    prefix = "to "
                case InflectionCode.subject_agreement:
                    inflection_type = None
                case InflectionCode.present_participle:
                    inflection_type = inflection.InflectionType.present_participle
                case InflectionCode.past_participle:
                    inflection_type = inflection.InflectionType.past_participle

            if inflection_type is not None:
                if " " in wrapped:
                    inflected = inflection.inflect_bracketed(wrapped, inflection_type)
                else:
                    inflected = inflection.inflect(wrapped, inflection_type)
            else:
                inflected = wrapped

            return prefix + inflected

        except ValueError as value_error:
            code_exception = InflectionCodeException(code_str)
            log.error(code_exception)
            raise code_exception from value_error

    return re.sub(r'%\(([@!\w]*)\)', apply_code, gloss)
