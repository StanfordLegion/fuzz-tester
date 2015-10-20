from random import *

from index_space import *
from field_space import *
from index_partition import *
from index_subspace import *
from logical_partition import *
from logical_region import *
from logical_subspace import *
from name_source import next_name
from region_requirement import *
from test_case import *

class TestGeneratorSettings():
    def __init__(self):
        self.seed = 1
        self.num_cases = 5
        self.max_fields = 4
        self.ind_min = 0
        self.ind_max = 100
        self.max_partitions = 3
        self.max_new_trees_per_task = 3
        self.max_task_children = 5
        self.max_region_requirements_per_task = 1
        self.max_fields_per_region_requirement = 3
        self.max_colors_per_partition = 3
        self.stop_constant = 10
        self.max_depth = 5
        self.privileges = ['READ_ONLY', 'READ_WRITE']
        self.coherences = ['EXCLUSIVE', 'ATOMIC', 'SIMULTANEOUS']

def generate_random_cases(settings):
    seed(settings.seed)
    cases = []
    for i in xrange(settings.num_cases):
        cases.append(random_case(i, settings))
    return cases

def random_case(test_num, settings):
    t = Task("top_level_task", [])
    logical_regions = random_logical_region_trees(t.name, settings)
    t.logical_regions_created = logical_regions
    subtasks = random_tasks(t.logical_regions_created, settings)
    t.child_tasks = subtasks
    case = TestCase("test_" + str(test_num), t)
    return case

def random_tasks(regions, settings):
    num_tasks = randint(1, settings.max_task_children)
    tasks = []
    for i in xrange(num_tasks):
        tasks.append(random_task(regions, settings))
    return tasks

def random_task(regions, settings):
    name = next_name('task')
    rrs = random_region_requirements(regions, settings)
    return Task(name, rrs)

def random_region_requirements(regions, settings):
    num_reqs = randint(0, settings.max_region_requirements_per_task)
    rrs = []
    for i in xrange(num_reqs):
        rrs.append(random_region_requirement(regions, settings))
    return rrs

def random_region_requirement(regions, settings):
    region_and_parent = pick_random_region_and_parent(regions, None, settings)
    region = region_and_parent[0]
    parent = region_and_parent[1]
    fields = random_fields(region, settings)
    privilege = settings.privileges[randint(0, len(settings.privileges) - 1)]
    coherence = settings.coherences[randint(0, len(settings.coherences) - 1)]
    return RegionRequirement(region, parent, fields, privilege, coherence)

def pick_random_region_and_parent(regions, parent, settings):
    region_ind = randint(0, len(regions) - 1)
    next_region = regions[region_ind]
    next_region.should_print()
    if should_stop(0, settings) or next_region.partitions == []:
        if parent is None:
            return (next_region, next_region)
        else:
            return (next_region, parent)
    next_partition = next_region.partitions[randint(0, len(next_region.partitions) - 1)]
    next_partition.should_print()
    next_regions = next_partition.subspaces
    next_parent = next_region
    return pick_random_region_and_parent(next_partition.subspaces, next_parent, settings)

def should_stop(depth, settings):
    i = randint(0, settings.stop_constant)
    return depth >= settings.max_depth or i == 0

def random_fields(region, settings):
    possible_fields = region.field_space.field_ids
    num_fields = randint(1, min(settings.max_fields_per_region_requirement, len(possible_fields)))
    return sample(set(possible_fields), num_fields)

def random_logical_region_trees(task_name, settings):
    num_trees = randint(1, settings.max_new_trees_per_task)
    logical_region_trees = []
    for i in xrange(0, num_trees):
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

def random_field_space(task_name, settings):
    name = next_name('field_space')
    num_fields = randint(1, settings.max_fields)
    field_ids = []
    for i in xrange(num_fields):
        field_ids.append(name + '_' + str(i))
    return FieldSpace(name, task_name, field_ids)
