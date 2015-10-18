from cpp_code import *

class FieldSpace():
    def __init__(self, name, task_name, field_ids):
        self.name = name
        self.task_name = task_name
        self.field_ids = field_ids

    def init_code(self):
        field_decl_str = cpp_var('FieldSpace ' + self.name)
        creation_call = cpp_funcall('runtime->create_field_space', [], [cpp_var('ctx')])
        assign = cpp_assign(field_decl_str, creation_call)
        allocate = cpp_block([create_allocator])
        return [assign, allocate]
