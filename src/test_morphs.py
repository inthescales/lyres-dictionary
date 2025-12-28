from lex_data.morphs.morph import Morph
from lex_data.morphs.morph_view import MorphView
from word_base.forms.formset import StemAndLeafFormSet, SingleFormSet
from word_base.senses.countability import Countability
from word_base.senses.gloss_provider import SingleGlossProvider
from word_base.senses.sense import NounSense, Sense
from word_base.element.classes.affix_classes import AffixPosition, DeriveClassData
from word_base.element.classes.element_class import ElementClass, ClassData

magnus: MorphView = MorphView(
        Morph(
            SingleFormSet("magn"),
            ClassData(ElementClass.adjective),
            Sense(SingleGlossProvider("large"))
        ),
    )

ify: MorphView = MorphView(
    Morph(
        StemAndLeafFormSet("ificat", "ify"),
        DeriveClassData(AffixPosition.suffix, ClassData(ElementClass.verb)),
        Sense(SingleGlossProvider("[make] %(@)"))
    )
)

ion: MorphView = MorphView(
    Morph(
        SingleFormSet("ion"),
        DeriveClassData(AffixPosition.suffix, ClassData(ElementClass.noun)),
        NounSense(SingleGlossProvider("the act or state of %(part)"), Countability.uncountable)
    )
)
