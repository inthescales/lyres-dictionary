from enum import auto, Enum

class ElementType(Enum):
    noun      = auto()
    adjective = auto()
    verb      = auto()
    number    = auto()
    derive    = auto()

    def is_root(self) -> bool:
        match self:
            case ElementType.noun, ElementType.adjective, ElementType.verb, ElementType.number:
                return True
            case ElementType.derive:
                return False

class TypeData:
    def __init__(self, morph_type: ElementType):
        self.type = morph_type

class DeriveTypeData(TypeData):
    def __init__(self, result_data: TypeData):
        TypeData.__init__(self, ElementType.derive)
        self.result_data = result_data
