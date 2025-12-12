import random

from src.tools.morphs.schemas.periods import periods_for # TODO: move this to language model?

# Returns a subset of the given list of senses having the most recent period
def most_recent(sense_list, language):
    periods = periods_for(language)

    sense_periods = []
    for sense in sense_list:
        if sense.period not in sense_periods:
            sense_periods.append(sense.period)

    latest_period = periods[0]
    for period in periods:
        if period in sense_periods:
            latest_period = period

    latest_senses = [s for s in sense_list if s.period == latest_period]
    old_senses = [s for s in sense_list if s not in latest_senses]

    return latest_senses

def random_latest(sense_list, language, seed):
    latest_senses = most_recent(sense_list, language)
    rand = random.Random(seed)
    return rand.choice(latest_senses)

def all_nonrecent(sense_list, language, seed):
    recent = most_recent(sense_list, language)
    return [s for s in sense_list if s not in recent]
