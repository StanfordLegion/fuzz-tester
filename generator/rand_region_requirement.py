from random import *

from region_requirement import *
from generator.utils import should_stop

def random_region_requirements(regions, settings):
    if regions != []:
        num_reqs = randint(0, settings.max_region_requirements_per_task)
    else:
        num_reqs = 0
    rrs = []
    for i in xrange(num_reqs):
        rrs.append(random_region_requirement(regions, settings))
    return rrs

def random_region_requirement(regions, settings):
    region_and_parent = pick_random_region_and_parent(regions, settings)
    region = region_and_parent[0]
    parent = region_and_parent[1]
    fields = random_fields(region, settings)
    privilege = settings.privileges[randint(0, len(settings.privileges) - 1)]
    coherence = settings.coherences[randint(0, len(settings.coherences) - 1)]
    return RegionRequirement(region, parent, fields, privilege, coherence)

def pick_random_region_and_parent(regions, settings):
    region_ind = randint(0, len(regions) - 1)
    region_to_select_from = regions[region_ind]
#    region_to_select_from.should_print()
    return (pick_random_region([region_to_select_from], settings), region_to_select_from)

def pick_random_region(regions, settings):
    next_region = regions[randint(0, len(regions) - 1)]
#    next_region.should_print()
    if should_stop(0, settings) or next_region.partitions == []:
        return next_region
    next_partition = next_region.partitions[randint(0, len(next_region.partitions) - 1)]
#    next_partition.should_print()
    next_regions = next_partition.subspaces
    return pick_random_region(next_regions, settings)

def random_fields(region, settings):
    possible_fields = region.field_space.field_ids
    num_fields = randint(1, min(settings.max_fields_per_region_requirement, len(possible_fields)))
    return sample(set(possible_fields), num_fields)

