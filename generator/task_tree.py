from random import randint

from generator.rand_logical_region import random_logical_region_trees
from generator.rand_region_requirement import random_region_requirements
from name_source import next_name
from task import Task

def random_tasks(regions, settings, depth):
    if depth >= settings.max_task_tree_depth:
        return []
    num_tasks = randint(1, settings.max_task_children)
    tasks = []
    for i in xrange(num_tasks):
        tasks.append(random_task(regions, settings, depth))
    return tasks

def random_task(regions, settings, depth):
    name = next_name('task')
    rrs = random_region_requirements(regions, settings)
    t = Task(name, rrs)
    t.logical_regions_created = random_logical_region_trees(t.name, settings)
    child_tasks = random_tasks(t.logical_regions_created, settings, depth+1)
    t.child_tasks = child_tasks
    return t
