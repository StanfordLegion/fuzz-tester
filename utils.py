import itertools

def flatten(iterable):
    return list(itertools.chain.from_iterable(iterable))

def flat_map(function, iterable):
    return flatten(map(function, iterable))
