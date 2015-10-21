from random import randint

from generator.rand_field_space import random_field_space
from generator.rand_index_tree import random_index_tree
from logical_partition import *
from logical_region import *
from logical_subspace import *
from name_source import next_name

def random_logical_region_trees(task_name, settings):
    num_trees = randint(1, settings.max_new_trees_per_task)
    logical_region_trees = []
    for i in xrange(1, num_trees + 1):
        logical_region_trees.append(random_logical_region_tree(task_name, settings))
    return logical_region_trees

def random_logical_region_tree(task_name, settings):
    field_space = random_field_space(task_name, settings)
    index_tree = random_index_tree(task_name, settings)
    logical_region_tree = make_logical_region_tree(task_name, field_space, index_tree)
    return logical_region_tree

def make_logical_region_tree(task_name, field_space, index_tree):
    name = next_name('logical_region')
    partitions = []
    for p in index_tree.partitions:
        partitions.append(make_logical_partition(task_name, field_space, p))
    return LogicalRegion(name, task_name, field_space, index_tree, partitions)

def make_logical_partition(task_name, field_space, partition):
    name = next_name('logical_partition')
    logical_subspaces = {}
    for i in partition.subspaces:
        logical_subspaces[i] = make_logical_subspace(task_name, field_space, partition.subspaces[i])
    return LogicalPartition(name, task_name, partition, logical_subspaces)

def make_logical_subspace(task_name, field_space, index_subspace):
    name = next_name('logical_subregion')
    partitions = []
    for p in index_subspace.partitions:
        partitions.append(make_logical_partition(task_name, field_space, p))
    return LogicalSubspace(name, task_name, field_space, index_subspace, partitions)
