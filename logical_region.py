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

    def should_print(self):
        self.is_needed = True
        self.field_space.is_needed = True
        self.index_space.is_needed = True

    def pretty_code(self):
        region_decl_str = cpp_var('LogicalRegion ' + self.name)
        args = [cpp_var('ctx'), cpp_var(self.index_space.name), cpp_var(self.field_space.name)]
        creation_call = cpp_funcall('runtime->create_logical_region', [], args)
        code = [cpp_assign(region_decl_str, creation_call)]
        for p in self.partitions:
            code.extend(p.init_code(self.name))
        return code

    def init_code(self):
        if self.is_needed:
            return self.pretty_code()
        else:
            return []
