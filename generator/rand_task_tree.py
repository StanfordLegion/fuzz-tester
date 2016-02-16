from random import randint, sample

from generator.rand_logical_region import random_logical_region_trees
from generator.rand_region_requirement import *
from name_source import next_name
from task import Task

def random_tasks(regions, settings, depth, parent_rrs=[], parent_name=None):
    if depth >= settings.max_task_tree_depth:
        return []
    num_tasks = randint(1, settings.max_task_children)
    tasks = []
    for i in xrange(num_tasks):
        tasks.append(random_task(regions, settings, depth, parent_rrs=parent_rrs, parent_name=None))
    return tasks

def random_task(regions, settings, depth, parent_rrs=[], parent_name=None):
    name = next_name( 'task' )
    region_requirements = random_region_requirements_no_alias(regions, settings)
    region_requirements_on_parent_regions = random_region_requirements_from_rrs_no_alias(parent_rrs, settings)
    # if parent_rrs:
        # region_requirements += parent_rrs
    # num_region_requirements_to_pass_on = int(len(region_requirements) * 0.5)
    # region_requirements = sample(region_requirements, num_region_requirements_to_pass_on)

    # Create task
    t = Task(name, region_requirements, parent_rrs)
    created_regions = random_logical_region_trees(t.name, settings)
    t.logical_regions_created = created_regions
    child_tasks = random_tasks(created_regions,
                               settings, depth+1,
                               parent_rrs=region_requirements,
                               parent_name=name)
    t.child_tasks = child_tasks
    return t
