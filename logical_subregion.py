from cpp_code import *

class LogicalSubregion():
    def __init__(self, name, task_name, field_space, index_space, partitions):
        self.name = name
        self.task_name = task_name
        self.field_space = field_space
        self.index_space = index_space
        self.partitions = partitions
        self.is_needed = False
        self.logical_region = None # assigned at creation time of logical_region
        self.logical_partition = None # assigned at creation time of logical_region
        self.color = None # assigned at creation time of logical_partition

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

    def shouldnt_print(self):
        self.is_needed = False
        self.index_space.is_needed = False

    def should_print(self):
        self.is_needed = True
        self.index_space.is_needed = True

    def any_child_is_needed(self):
        child_is_needed = False
        for p in self.partitions:
            p.should_print_if_any_child_is_needed()
            if p.is_needed:
                child_is_needed = True
        return child_is_needed

    def pretty_code(self,):
        init_call = 'LogicalRegion ' + self.name + ' = runtime->get_logical_subregion_by_color(ctx, ' + self.logical_partition.name + ', ' + str(self.color) + ')'
        naming_call = cpp_funcall('runtime->attach_name', [], [self.name, '"' + self.name + '"'])
        registration_value_pair = cpp_value_pair('LogicalRegion', self.name)
        registration_call = cpp_funcall('scope.logical_regions.insert', [], [registration_value_pair])
        code = [init_call, naming_call, registration_call]
        for p in self.partitions:
            code.extend(p.init_code())
        return code

    def retrieve_code(self):
        code = []
        # if self.logical_region:
        #     code += self.logical_region.retrieve_code()
        region_decl_str = cpp_var('LogicalRegion ' + self.name)
        retrieval_call = cpp_funcall('scope.logical_regions.at', [], ['"' + self.name + '"'])
        assign_call = cpp_assign(region_decl_str, retrieval_call)
        code += [assign_call]
        return code

    def init_code(self):
        if self.is_needed:
            return self.pretty_code()
        else:
            return []

    # def init_code_with_parents(self):
    #     code = []
    #     if self.logical_region:
    #         code.extend(self.logical_region.init_code_with_parents())
    #     if self.logical_partition:
    #         code.extend(self.logical_partition.init_code_with_parents())
    #     code.extend(self.init_code())
    #     return code

    def set_logical_region(self, logical_region):
        self.logical_region = logical_region
        for partition in self.partitions:
            partition.set_logical_region(logical_region)

    def set_logical_partition(self, logical_partition):
        self.logical_partition = logical_partition
