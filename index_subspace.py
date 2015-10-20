from cpp_code import *

class IndexSubspace():
    def __init__(self, name, task_name, start, end, partitions):
        self.name = name
        self.task_name = task_name
        self.start = start
        self.end = end
        self.partitions = partitions
        self.is_needed = False

    def pretty_code(self, parent_name, color):
        init_call = 'runtime->get_index_subspace(ctx, ' + parent_name + ', ' + str(color) + ')'
        is_init = cpp_assign('IndexSpace ' + self.name, init_call)
        code = [is_init]
        for p in self.partitions:
            code.extend(p.init_code(self.name))
        return code

    def init_code(self, parent_name, color):
        if self.is_needed:
            return self.pretty_code(parent_name, color)
        else:
            return []
