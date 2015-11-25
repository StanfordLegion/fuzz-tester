from random import *

from index_space import *
from field_space import *
from generator.rand_logical_region import random_logical_region_trees
from generator.rand_task_tree import random_tasks
from generator.test_generator_settings import TestGeneratorSettings
from generator.utils import should_stop
from index_partition import *
from index_subspace import *
from logical_partition import *
from logical_region import *
from logical_subspace import *
from name_source import next_name
from region_requirement import *
from test_case import *

def generate_random_cases(settings):
    seed(settings.seed)
    cases = []
    for i in xrange(settings.num_cases):
        cases.append(random_case(i, settings))
    return cases

def random_case(test_num, settings):
    t = Task('top_level_task', [])
    logical_regions = random_logical_region_trees(t.name, settings)
    t.logical_regions_created = logical_regions
    t.child_tasks = random_tasks(t.logical_regions_created, settings, 0)
    t.decide_what_should_print()
    case = TestCase('test_' + str(test_num), t)
    return case
