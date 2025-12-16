from src.word import Word

# Render a word's contents into entry text format
def render(word: Word) -> str:
	head_text = f"{word.form()} ({word.type()})"
	body_text = f"{word.definition()}"
	return head_text + "\n" + body_text

# Model representing a dictionary entry for a given word.
# Is responsible for taking the word's data and presenting it in proper textual
# format. Also contains metadata related to display and publishing.
class Entry:
	def __init__(self, word: Word):
		self.word: Word = word				# The word represented by the entry
		self.text: str = render(word)		# Display text
		self.metadata: dict = {}			# Presentation metadata
