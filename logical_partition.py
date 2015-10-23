from itertools import chain

from cpp_code import *

class LogicalPartition():
    def __init__(self, name, task_name, index_partition, subspaces):
        self.name = name
        self.task_name = task_name
        self.subspaces = subspaces
        self.index_partition = index_partition
        self.is_needed = False

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
            
    def should_print(self):
        self.is_needed = True
        self.index_partition.is_needed = True

    def pretty_code(self, parent_name):
        init_call = 'runtime->get_logical_partition(ctx, ' + parent_name + ', ' + self.index_partition.name + ')'
        partition_init = cpp_assign('LogicalPartition ' + self.name, init_call)
        subspace_init = []
        for color in self.subspaces:
            s = self.subspaces[color]
            subspace_init.extend(s.init_code(self.name, color))
        return [partition_init] + subspace_init

    def init_code(self, parent_name):
        if self.is_needed:
            return self.pretty_code(parent_name)
        else:
            return []
