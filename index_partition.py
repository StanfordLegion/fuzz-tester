class IndexPartition():
    def __init__(self, name, task_name, subspaces):
        self.name = name
        self.task_name = task_name
        self.subspaces = subspaces
        self.is_needed = False

    def color_init(self, dom_name, color, start, end):
        lhs = dom_name + '[' + str(color) + '] = '
        rhs = 'Domain::from_rect<1>(Rect<1>(Point<1>(' + str(start) + '), Point<1>(' + str(end) + ')))'
        return lhs + rhs

    def domain_coloring_init(self):
        dom_name = self.name + '_coloring'
        domain_init = 'DomainColoring ' + dom_name
        code = [domain_init]
        for color in self.subspaces:
            s = self.subspaces[color]
            code.append(self.color_init(dom_name, color, s.start, s.end))
        return code

    def color_max(self):
        return max(self.subspaces, key=self.subspaces.get)

    def color_min(self):
        return min(self.subspaces, key=self.subspaces.get)

    def pretty_code(self, parent_name):
        color_dom_name = self.name + '_color_domain'
        dom_name = self.name + '_coloring'
        dom_init = 'Domain ' + color_dom_name + ' = Domain::from_rect<1>(Rect<1>(Point<1>(' + str(self.color_min()) + '), Point<1>(' + str(self.color_max()) + ')))'
        part_init = 'IndexPartition ' + self.name + ' = ' + 'runtime->create_index_partition(ctx, ' + parent_name + ', ' + color_dom_name + ', ' + dom_name + ', false)'
        code = self.domain_coloring_init() + [dom_init, part_init]
        for color in self.subspaces:
            s = self.subspaces[color]
            code.extend(s.init_code(self.name, color))
        return code

    def init_code(self, parent_name):
        if self.is_needed:
            return self.pretty_code(parent_name)
        else:
            return []
