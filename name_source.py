next_name_suffix = 0

def next_name(prefix):
    global next_name_suffix
    name = prefix + '_' + str(next_name_suffix)
    next_name_suffix += 1
    return name
