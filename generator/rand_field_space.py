from random import randint

from field_space import FieldSpace
from name_source import next_name

def random_field_space(task_name, settings):
    name = next_name('field_space')
    num_fields = randint(1, settings.max_fields)
    field_ids = []
    for i in xrange(num_fields):
        field_ids.append(name + '_' + str(i))
    return FieldSpace(name, task_name, field_ids)
