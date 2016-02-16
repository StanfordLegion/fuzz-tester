from collections import Counter

prefix_counter = Counter()


def next_name(prefix):
    global prefix_counter
    assert (prefix and len(prefix) > 0)
    name = prefix + '_' + str(prefix_counter[prefix])
    prefix_counter[prefix] += 1
    return name
