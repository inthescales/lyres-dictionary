class Color:
	red = '\033[91m'
	green = '\033[92m'
	yellow = '\033[93m'

	end = '\033[0m'

def color_text(color, text):
	return color + text + Color.end
