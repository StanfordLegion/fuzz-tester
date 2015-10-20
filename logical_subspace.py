class LogicalSubspace():
    def __init__(self, name, task_name, field_space, index_space, partitions):
        self.name = name
        self.task_name = task_name
        self.field_space = field_space
        self.index_space = index_space
        self.partitions = partitions
        self.is_needed = False

    def should_print(self):
        self.is_needed = True
        self.index_space.is_needed = True

    def pretty_code(self, parent_name, color):
        init_call = 'LogicalRegion ' + self.name + ' = runtime->get_logical_subregion_by_color(ctx, ' + parent_name + ', ' + str(color) + ')'
        code = [init_call]
        for p in self.partitions:
            code.extend(p.init_code(self.name))
        return code

    def init_code(self, parent_name, color):
        if self.is_needed:
            return self.pretty_code(parent_name, color)
        else:
            return []
