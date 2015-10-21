class TestGeneratorSettings():
    def __init__(self):
        self.seed = 1
        self.num_cases = 1
        self.max_fields = 20
        self.ind_min = 0
        self.ind_max = 1000
        self.max_partitions = 10
        self.max_new_trees_per_task = 20
        self.max_task_children = 5
        self.max_region_requirements_per_task = 1
        self.max_fields_per_region_requirement = 100
        self.max_colors_per_partition = 5
        self.stop_constant = 30
        self.max_depth = 3
        self.max_task_tree_depth = 3
        self.privileges = ['READ_ONLY', 'READ_WRITE']
        self.coherences = ['EXCLUSIVE', 'ATOMIC', 'SIMULTANEOUS']
