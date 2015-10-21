from cpp_code import *

class FieldSpace():
    def __init__(self, name, task_name, field_ids):
        self.name = name
        self.task_name = task_name
        self.field_ids = field_ids
        self.is_needed = False

    def allocate_fields(self):
        allocate_stmts = []
        for field in self.field_ids:
            allocate_stmts.append('allocator.allocate_field(sizeof(int),' + field + ')')
        return allocate_stmts

    def init_code(self):
        if self.is_needed:
            field_decl_str = cpp_var('FieldSpace ' + self.name)
            creation_call = cpp_funcall('runtime->create_field_space', [], [cpp_var('ctx')])
            assign = cpp_assign(field_decl_str, creation_call)
            create_allocator = cpp_assign(cpp_var('FieldAllocator allocator'), cpp_funcall('runtime->create_field_allocator', [], [cpp_var('ctx'), cpp_var(self.name)]))
            allocate = cpp_block([create_allocator] + self.allocate_fields())
            return [assign, allocate]
        else:
            return []
