from random import *

from name_source import *
from region_requirement import *
from generator.utils import should_stop


def random_region_requirements(regions, settings):
    if regions != []:
        num_reqs = randint(0, settings.max_region_requirements_per_task)
    else:
        num_reqs = 0
    rrs = []
    for i in xrange(num_reqs):
        rrs.append(random_region_requirement(regions, None, settings))
    return rrs


def random_region_requirements_no_alias(regions, settings):
    rrs = random_region_requirements(regions, settings)
    no_alias_rrs = delete_aliasing_requirements(regions, rrs)
    return no_alias_rrs


def random_region_requirements_from_rrs_no_alias(parent_rrs, settings):
    regions_and_fields = [(rr.region, rr.fields) for rr in parent_rrs]
    rrs = []
    for region, fields in regions_and_fields:
        rrs += [random_region_requirement([region], fields, settings)]
    regions = [rr.region for rr in parent_rrs]
    no_alias_rrs = delete_aliasing_requirements(regions, rrs)
    return no_alias_rrs


def random_region_requirement(on_regions, on_fields, settings):
    assert( len(on_regions) > 0 )
    region, parent = pick_random_region_and_parent(on_regions, settings)
    if on_fields:
        fields = random_sample_of_fields(on_fields, settings)
    else:
        fields = random_fields(region, settings)
    privilege = settings.privileges[randint(0, len(settings.privileges) - 1)]
    coherence = settings.coherences[randint(0, len(settings.coherences) - 1)]
    name = next_name("region_requirement")
    return RegionRequirement(name, region, parent, fields, privilege, coherence)


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
    return random_sample_of_fields(possible_fields, settings)


def random_sample_of_fields(fields, settings):
    num_fields = randint(1, min(settings.max_fields_per_region_requirement, len(fields)))
    return sample(set(fields), num_fields)
