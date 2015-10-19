from random import *

from index_space import *
from field_space import *
from logical_region import *
from region_requirement import *
from test_case import *

next_name_suffix = 0

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
    region = regions[randint(0, len(regions) - 1)]
    privilege = settings.privileges[randint(0, len(settings.privileges) - 1)]
    coherence = settings.coherences[randint(0, len(settings.coherences) - 1)]
    return RegionRequirement(region, privilege, coherence)

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
        self.max_task_children = 5
        self.max_region_requirements_per_task = 1
        self.privileges = ['READ_ONLY', 'READ_WRITE']
        self.coherences = ['EXCLUSIVE', 'ATOMIC', 'SIMULTANEOUS']

