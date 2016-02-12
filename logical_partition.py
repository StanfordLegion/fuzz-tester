from itertools import chain

from cpp_code import *

class LogicalPartition():
    def __init__(self, name, task_name, index_partition, subspaces):
        self.name = name
        self.task_name = task_name
        self.subspaces = subspaces
        self.index_partition = index_partition
        self.is_needed = False
        self.logical_region = None # is assigned when logical region is created

    def should_print_if_any_child_is_needed(self):
        if self.any_child_is_needed():
            self.should_print()

    def any_child_is_needed(self):
        child_is_needed = False
        for color in self.subspaces:
            s = self.subspaces[color]
            s.should_print_if_any_child_is_needed()
            if s.is_needed:
                child_is_needed = True
        return child_is_needed

    def shouldnt_print_anything(self):
        self.shouldnt_print()
        map(lambda c: self.subspaces[c].shouldnt_print_anything(), self.subspaces)

    def shouldnt_print(self):
        self.is_needed = False
        self.index_partition.is_needed = False

    def should_print(self):
        self.is_needed = True
        self.index_partition.is_needed = True

    def pretty_code(self):
        init_call = 'runtime->get_logical_partition(ctx, ' + self.logical_region.name + ', ' + self.index_partition.name + ')'
        partition_init = cpp_assign('LogicalPartition ' + self.name, init_call)
        naming_call = cpp_funcall('runtime->attach_name', [], [self.name, '"' + self.name + '"'])
        registration_value_pair = cpp_value_pair('LogicalPartition', self.name)
        registration_call = cpp_funcall('scope.logical_partitions.insert', [], [registration_value_pair])
        subspace_init = []
        for color in self.subspaces:
            s = self.subspaces[color]
            subspace_init.extend(s.init_code())
        return [partition_init, naming_call, registration_call] + subspace_init

    def init_code(self):
        if self.is_needed:
            return self.pretty_code()
        else:
            return []

    def retrieve_code(self):
        region_decl_str = cpp_var('LogicalPartition ' + self.name)
        retrieval_call = cpp_funcall('scope.logical_partitions.at', [], ['"' + self.name + '"'])
        assign_call = cpp_assign(region_decl_str, retrieval_call)
        return [assign_call]

    def set_logical_region(self, logical_region):
        self.logical_region = logical_region
        for subspace_index in self.subspaces:
            subspace = self.subspaces[subspace_index]
            subspace.color = subspace_index
            subspace.set_logical_region(logical_region)
            subspace.set_logical_partition(self)

    def init_code_with_parents(self):
        code = []
        if self.logical_region:
            code.extend(self.logical_region.init_code_with_parents())
        code.extend( self.init_code() )
        return code