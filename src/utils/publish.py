from collections.abc import Callable

from generate import Entry

def publish(entry_gen: Callable[[], Entry]):
    """Using the given entry generator callable, generate an entry and publish it online."""
    import botbuddy  # Defer import since it's a bit slow

    def post_gen() -> dict:
        """Convert entry contents into the form Botbuddy takes."""
        entry = entry_gen()
        return {"content": entry.text, "metadata": entry.metadata}

    botbuddy.post(post_gen)
