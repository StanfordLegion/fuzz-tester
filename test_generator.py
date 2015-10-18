from random import *

from index_space import *
from field_space import *
from logical_region import *
from test_case import *

next_name_suffix = 0

def generate_random_cases(settings):
    seed(settings.seed)
    cases = []
    for i in xrange(settings.num_cases):
        cases.append(random_case(i, settings))
    return cases

def random_case(test_num, settings):
    t = Task("top_level_task")
    logical_regions = random_logical_region_trees(t.name, settings)
    t.logical_regions_created = logical_regions
    case = TestCase("test_" + str(test_num), t)
    return case

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
    return LogicalRegion(name, task_name, field_space, index_tree)

def random_index_tree(task_name, settings):
    start = randint(settings.ind_min, settings.ind_max)
    end = randint(start, settings.ind_max)
    name = next_name('index_space')
    return IndexSpace(name, task_name, start, end)
    
def random_field_space(task_name, settings):
    name = next_name('field_space')
    num_fields = randint(1, settings.max_fields)
    field_ids = []
    for i in xrange(num_fields):
        field_ids.append(name + '_' + str(i))
    return FieldSpace(name, task_name, field_ids)

def next_name(prefix):
    global next_name_suffix
    name = prefix + '_' + str(next_name_suffix)
    next_name_suffix += 1
    return name

class TestGeneratorSettings():
    def __init__(self):
        self.seed = 0
        self.num_cases = 1
        self.max_fields = 4
        self.ind_min = 0
        self.ind_max = 100
        self.max_new_trees_per_task = 3

