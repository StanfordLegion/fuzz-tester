class IndexPartition():
    def __init__(self, name, task_name, subspaces):
        self.name = name
        self.task_name = task_name
        self.subspaces = subspaces
        self.is_needed = False

    def color_init(self, dom_name, color, start, end):
        lhs = dom_name + '[' + str(color) + '] = '
        rhs = 'Rect<1>(' + str(start) + ',' + str(end) + ')'
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
        max_color = -10
        for color in self.subspaces:
            if color > max_color:
                max_color = color
        return max_color

    def color_min(self):
        min_color = 100000000
        for color in self.subspaces:
            if color < min_color:
                min_color = color
        return min_color

    def is_disjoint(self):
        disjoint = True
        for color1 in self.subspaces:
            for color2 in self.subspaces:
                sub1 = self.subspaces[color1]
                sub2 = self.subspaces[color2]
                if color1 != color2 and sub1.overlaps(sub2):
                    disjoint = False
        return disjoint

    def pretty_code(self, parent_name):
        color_dom_name = self.name + '_color_domain'
        dom_name = self.name + '_coloring'
        dom_init = 'Domain ' + color_dom_name + ' = Rect<1>(' + str(self.color_min()) + ',' + str(self.color_max()) + ')'
        part_init = 'IndexPartition ' + self.name + ' = ' + 'runtime->create_index_partition(ctx, ' + parent_name + ', ' + color_dom_name + ', ' + dom_name + ', ' + str(self.is_disjoint()).lower() + ')'
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
