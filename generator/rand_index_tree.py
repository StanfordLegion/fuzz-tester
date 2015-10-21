from random import randint

from index_partition import IndexPartition
from index_space import IndexSpace
from index_subspace import IndexSubspace
from name_source import next_name
from generator.utils import should_stop

def random_index_tree(task_name, settings):
    start = randint(settings.ind_min, settings.ind_max)
    end = randint(start, settings.ind_max)
    name = next_name('index_space')
    if should_stop(0, settings):
        partitions = []
    else:
        partitions = random_index_partitions(task_name, 0, start, end, settings)
    return IndexSpace(name, task_name, start, end, partitions)

def random_index_partitions(task_name, depth, start, end, settings):
    parts = []
    num_parts = randint(0, settings.max_partitions)
    for i in xrange(0, num_parts):
        parts.append(random_index_partition(task_name, depth+1, start, end, settings))
    return parts

def random_index_partition(task_name, depth, start, end, settings):
    num_colors = randint(1, settings.max_colors_per_partition)
    subspaces = {}
    for i in xrange(0, num_colors):
        subspaces[i] = random_index_subspace(task_name, depth+1, start, end, settings)
    part_name = next_name('index_partition')
    return IndexPartition(part_name, task_name, subspaces)

def random_index_subspace(task_name, depth, start, end, settings):
    sub_start = randint(start, end)
    sub_end = randint(sub_start, end)
    name = next_name('index_subspace')
    if should_stop(depth, settings):
        partitions = []
    else:
        partitions = random_index_partitions(task_name, depth+1, sub_start, sub_end, settings)
    return IndexSubspace(name, task_name, sub_start, sub_end, partitions)
