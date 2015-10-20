from itertools import chain

from cpp_code import *

class IndexSpace():
    def __init__(self, name, task_name, ind_start, ind_end, partitions):
        self.name = name
        self.task_name = task_name
        self.ind_start = ind_start
        self.ind_end = ind_end
        self.partitions = partitions
        self.is_needed = False

    def pretty_code(self):
        ind_decl_string = cpp_var('IndexSpace ' + self.name)
        ctx = cpp_var('ctx')
        elem_rect = 'Rect<1>(Point<1>(' + str(self.ind_start) + '), ' + 'Point<1>(' + str(self.ind_end) + '))'
        domain = cpp_var('Domain::from_rect<1>(' + elem_rect + ')')
        creation_call = cpp_funcall('runtime->create_index_space', [], [ctx, domain])
        partition_init = list(chain(*map(lambda p: p.init_code(self.name), self.partitions)))
        return [cpp_assign(ind_decl_string, creation_call)] + partition_init

    def init_code(self):
        if self.is_needed:
            return self.pretty_code()
        else:
            return ['']
