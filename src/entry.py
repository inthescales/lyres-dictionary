class Entry():
	def __init__(self, word):
		self.word = word

	def text(self):
		line1 = f"{self.word.form()} ({self.word.type()})"
		line2 = f"{self.word.definition()}"
		return line1 + "\n" + line2
