def publish(entry):
	import botbuddy # Defer import since it's a bit slow
	botbuddy.post(entry)
