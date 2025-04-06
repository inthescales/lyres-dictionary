# Randomly filter out morphs with less than 100% frequency
def for_morph(morph):
    frequencies = {
        "homophonic": 10,
        "poetic": 10,
        "rare": 10,
        "super-rare": 1
    }

    frequency = 100
    for tag in morph.tags():
        if tag in frequencies:
            frequency = min(frequency, frequencies[tag])

    return frequency
