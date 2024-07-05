import src.evolutor.evolutor as evolutor
import src.tools.tablemaker.table as table

from src.evolutor.engine.config import Config

def make_table_oe_ne(inputs):
    config = Config(locked=False)

    oe_phonemes = []
    for input in inputs:
        phonemes = evolutor.oe_orth_to_oe_phone(input, config)
        oe_phonemes.append(phonemes)

    me_phonemes = []
    for oe in oe_phonemes:
        phonemes = evolutor.oe_phone_to_me_phone(oe, config)
        me_phonemes.append(phonemes)

    modern_forms = []
    for me in me_phonemes:
        spelling = evolutor.me_phone_to_ne_orth(me, config)
        modern_forms.append(spelling)

    oe_forms = [form.replace("|", "") for form in inputs]
    oe_output = ["/" + "".join([x.value for x in word]) + "/" for word in oe_phonemes]
    me_output = ["/" + "".join([x.value for x in word]) + "/" for word in me_phonemes]
    output_table = table.make_table([
        table.TableColumn("OE written", oe_forms),
        table.TableColumn("OE phonemes", oe_output),
        table.TableColumn("ME phonemes", me_output),
        table.TableColumn("Modern form", modern_forms),
    ])

    return output_table
