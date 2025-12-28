from word import Word

def render(word: Word) -> str:
    """Renders the given word into a string form for presentation"""

    head_text = f"{word.form} ({word.type.string})"
    body_text = f"{word.definition}"
    return head_text + "\n" + body_text

class Entry:
    """
    Model representing a dictionary entry for a given word.
    Responsible for taking the word's data and presenting it in proper textual
    format. Also contains metadata related to display and publishing.
    """

    def __init__(self, word: Word):
        self.word: Word = word  # The word represented by the entry
        self.text: str = render(word)  # Display text
        self.metadata: dict = {}  # Presentation metadata
