class LogicalSubspace():
    def __init__(self, name, task_name, field_space, index_space, partitions):
        self.name = name
        self.task_name = task_name
        self.field_space = field_space
        self.index_space = index_space
        self.partitions = partitions
        self.is_needed = False

    def is_root_of(self, region):
        if region.name == self.name:
            return True
        for p in self.partitions:
            for s in p.subspaces:
                if p.subspaces[s].is_root_of(region):
                    return True
        return False

    def shouldnt_print_anything(self):
        self.shouldnt_print()
        map(lambda p: p.shouldnt_print_anything(), self.partitions)

    def should_print_if_any_child_is_needed(self):
        if self.any_child_is_needed():
            self.should_print()

    def shouldnt_print(self):
        self.is_needed = False
        self.index_space.is_needed = False
            
    def should_print(self):
        self.is_needed = True
        self.index_space.is_needed = True

    def any_child_is_needed(self):
        child_is_needed = False
        for p in self.partitions:
            p.should_print_if_any_child_is_needed()
            if p.is_needed:
                child_is_needed = True
        return child_is_needed
        
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
