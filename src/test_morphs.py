from lex_data.morphs.morph import Morph
from lex_data.morphs.morph_view import MorphView
from word_base.forms.formset import LeafAndStemFormSet, SingleFormSet
from word_base.senses.countability import Countability
from word_base.senses.gloss_provider import SingleGlossProvider
from word_base.senses.sense import NounSense, Sense
from word_base.lex_class.lex_class import DeriveClassData, LexClass, ClassData

magnus: MorphView = MorphView(
        Morph(
            SingleFormSet("magn"),
            ClassData(LexClass.adjective),
            Sense(SingleGlossProvider("large"))
        ),
    )

ify: MorphView = MorphView(
    Morph(
        LeafAndStemFormSet("ificat", "ify"),
        DeriveClassData(ClassData(LexClass.verb)),
        Sense(SingleGlossProvider("[make] %(@)"))
    )
)

ion: MorphView = MorphView(
    Morph(
        SingleFormSet("ion"),
        DeriveClassData(ClassData(LexClass.noun)),
        NounSense(SingleGlossProvider("the act or state of %(part)"), Countability.uncountable)
    )
)
