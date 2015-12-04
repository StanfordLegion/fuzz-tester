from cpp_code import *

class RegionRequirement():
    def __init__(self, region, parent_region, fields, privilege, coherence):
        self.region = region
        self.parent_region = parent_region
        self.fields = fields
        self.privilege = privilege
        self.coherence = coherence

    def add_fields(self, requirement_num, launcher_name):
        field_add_stmts = []
        for f in self.fields:
            field_add_stmts.append(launcher_name + '.region_requirements[' + str(requirement_num) + '].add_field(' + f + ')')
        return field_add_stmts

    def should_print(self):
        self.region.should_print()

    def init_code(self, requirement_num, launcher_name):
        rr = cpp_funcall('RegionRequirement', [], [self.region.name, self.privilege, self.coherence, self.parent_region.name])
        add_rr = cpp_funcall(launcher_name + '.add_region_requirement', [], [rr])
        return [add_rr] + self.add_fields(requirement_num, launcher_name)

def delete_aliasing_requirements(regions, rrs):
    no_alias_rrs = []
    for i in xrange(len(rrs)):
        rr = rrs[i]
        if i == len(rrs) - 1 or not any_aliases_in_list(regions, rr, rrs[i+1:]):
            no_alias_rrs.append(rr)
    return no_alias_rrs

def any_aliases_in_list(regions, rr, rrs):
    for other in rrs:
        if rr_alias(regions, rr, other):
            return True
    return False

def rr_alias(regions, l, r):
    l_root = find_root(regions, l)
    r_root = find_root(regions, r)
    if l_root.name != r_root.name:
        return False
    return fields_overlap(l, r)

def fields_overlap(l, r):
    lfs = set(l.fields)
    rfs = set(r.fields)
    return len(lfs.intersection(rfs)) > 0

def find_root(regions, rr):
    for region in regions:
        if region.is_root_of(rr.region):
            return region
    raise ValueError('No root for ' + str(rr) + ' in ' + str(regions))
