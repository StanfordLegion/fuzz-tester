from cpp_code import *

class LogicalRegion():
    def __init__(self, name, task_name, field_space, index_space):
        self.name = name
        self.task_name = task_name
        self.field_space = field_space
        self.index_space = index_space

    def init_code(self):
        region_decl_str = cpp_var('LogicalRegion ' + self.name)
        args = [cpp_var('ctx'), cpp_var(self.index_space.name), cpp_var(self.field_space.name)]
        creation_call = cpp_funcall('runtime->create_logical_region', [], args)
        return cpp_assign(region_decl_str, creation_call)
