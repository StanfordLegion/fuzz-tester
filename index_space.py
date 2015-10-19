from cpp_code import *

class IndexSpace():
    def __init__(self, name, task_name, ind_start, ind_end):
        self.name = name
        self.task_name = task_name
        self.ind_start = ind_start
        self.ind_end = ind_end

    def init_code(self):
        ind_decl_string = cpp_var('IndexSpace ' + self.name)
        ctx = cpp_var('ctx')
        elem_rect = 'Rect<1>(Point<1>(' + str(self.ind_start) + '), ' + 'Point<1>(' + str(self.ind_end) + '))'
        domain = cpp_var('Domain::from_rect<1>(' + elem_rect + ')')
        creation_call = cpp_funcall('runtime->create_index_space', [], [ctx, domain])
        return cpp_assign(ind_decl_string, creation_call)
