from cpp_code import *

class LogicalRegion():
    def __init__(self, name, task_name, field_space, index_space, partitions):
        self.name = name
        self.task_name = task_name
        self.parent = self
        self.field_space = field_space
        self.index_space = index_space
        self.is_needed = False
        self.partitions = partitions
        for partition in self.partitions:
            partition.set_logical_region(self)

    def is_root_of(self, region):
        if region.name == self.name:
            return True
        for p in self.partitions:
            for s in p.subspaces:
                if p.subspaces[s].is_root_of(region):
                    return True
        return False

    def shouldnt_print_anything(self):
        self.shouldnt_print()
        map(lambda p: p.shouldnt_print_anything(), self.partitions)

    def should_print_if_any_child_is_needed(self):
        if self.any_child_is_needed():
            self.should_print()

    def should_print(self):
        self.is_needed = True
        self.field_space.is_needed = True
        self.index_space.is_needed = True

    def shouldnt_print(self):
        self.is_needed = False
        self.field_space.is_needed = False
        self.index_space.is_needed = False

    def any_child_is_needed(self):
        child_is_needed = False
        for p in self.partitions:
            p.should_print_if_any_child_is_needed()
            if p.is_needed:
                child_is_needed = True
        return child_is_needed

    def collect_subregions(self):
        sub_regions = []
        for partition in self.partitions:
            sub_regions += partition.collect_subregions()
        return sub_regions

    def pretty_code(self):
        region_decl_str = cpp_var('LogicalRegion ' + self.name)
        args = [cpp_var('ctx'), cpp_var(self.index_space.name), cpp_var(self.field_space.name)]
        creation_call = cpp_funcall('runtime->create_logical_region', [], args)
        naming_call = cpp_funcall('runtime->attach_name', [], [self.name, '"' + self.name + '"'])
        registration_call = "scope." + self.name + " = " + self.name
        code = [cpp_assign(region_decl_str, creation_call), naming_call, registration_call]
        for p in self.partitions:
            code += p.init_code()
        return code

    def retrieve_code(self):
        region_declaration = cpp_var("LogicalRegion " + self.name)
        retrieval_call = "scope." + self.name
        assign_call = cpp_assign(region_declaration, retrieval_call)
        return [assign_call]

    def init_code(self, task_name=None):
        if self.is_needed and task_name == self.task_name:
            return self.pretty_code()
        else:
            return []

    def init_code_with_parents(self):
        return self.init_code()
