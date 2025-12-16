from collections.abc import Callable

from src.generate import Entry

def publish(entry_gen: Callable[[], Entry]):
	import botbuddy # Defer import since it's a bit slow

	# Convert entry contents into the form botbuddy takes
	def post_gen() -> dict:
		entry = entry_gen()
		return {"content": entry.text, "metadata": entry.metadata}

	botbuddy.post(post_gen)
