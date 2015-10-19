from cpp_code import *

class RegionRequirement():
    def __init__(self, region, fields, privilege, coherence):
        self.region = region
        self.fields = fields
        self.privilege = privilege
        self.coherence = coherence

    def add_fields(self, requirement_num, launcher_name):
        field_add_stmts = []
        for f in self.fields:
            field_add_stmts.append(launcher_name + '.region_requirements[' + str(requirement_num) + '].add_field(' + f + ')')
        return field_add_stmts

    def init_code(self, requirement_num, launcher_name):
        rr = cpp_funcall('RegionRequirement', [], [self.region.name, self.privilege, self.coherence, self.region.name])
        add_rr = cpp_funcall(launcher_name + '.add_region_requirement', [], [rr])
        return [add_rr] + self.add_fields(requirement_num, launcher_name)
