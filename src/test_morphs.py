from src.morphs.morph_view import Morph, MorphView
from src.forms.formset import LeafAndStemFormSet, SingleFormSet
from src.senses.countability import Countability
from src.senses.gloss_provider import SingleGlossProvider
from src.senses.sense import NounSense, Sense
from src.types.element_type import DeriveTypeData, ElementType, TypeData

magnus: MorphView = MorphView(
        Morph(
            SingleFormSet("magn"),
            TypeData(ElementType.adjective),
            Sense(SingleGlossProvider("large"))
        ),
    )

ify: MorphView = MorphView(
    Morph(
        LeafAndStemFormSet("ificat", "ify"),
        DeriveTypeData(TypeData(ElementType.verb)),
        Sense(SingleGlossProvider("[make] %(@)"))
    )
)

ion: MorphView = MorphView(
    Morph(
        SingleFormSet("ion"),
        DeriveTypeData(TypeData(ElementType.noun)),
        NounSense(SingleGlossProvider("the act or state of %(part)"), Countability.uncountable)
    )
)
