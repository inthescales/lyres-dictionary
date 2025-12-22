from src.morphs.morph_view import Morph, MorphView
from src.forms.formset import LeafAndStemFormSet, SingleFormSet
from src.senses.countability import Countability
from src.senses.gloss_provider import SingleGlossProvider
from src.senses.sense import NounSense, Sense

magnus: MorphView = MorphView(
        Morph(
            SingleFormSet("magn"),
            Sense(SingleGlossProvider("large"))
        )
    )

ify: MorphView = MorphView(
    Morph(
        LeafAndStemFormSet("ificat", "ify"),
        Sense(SingleGlossProvider("[make] %(@)"))
    )
)

ion: MorphView = MorphView(
    Morph(
        SingleFormSet("ion"),
        NounSense(SingleGlossProvider("the act or state of %(part)"), Countability.uncountable)
    )
)
