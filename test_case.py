from itertools import chain
from utils import *
from cpp_code import *
from task import Task

def run_test_case(case):
    print case.pretty_string()

class TestCase():
    def __init__(self, name, top_level_task):
        self.name = name
        self.top_level_task = top_level_task
        self.top_level_task.is_top_level = True

    def pretty_field_id_enums(self):
        all_field_spaces = filter(lambda fs: fs.is_needed, self.top_level_task.collect_field_spaces())
        return map(lambda x: cpp_enum(x.name.upper(), map(lambda y: cpp_var(y), x.field_ids)), all_field_spaces)

    def pretty_task_id_enum(self):
        tasks = self.top_level_task.collect_tasks()
        task_id_names = map(lambda t: t.id(), tasks)
        return cpp_enum("TASK_ID", task_id_names)

    def pretty_task_functions(self):
        all_tasks = self.top_level_task.collect_tasks()
        return map(lambda t: t.task_function(), all_tasks)

    def pretty_main(self):
        main_args = [cpp_formal_param(cpp_int(), cpp_var("argc")),
                     cpp_formal_param(cpp_ptr(cpp_ptr(cpp_char())), cpp_var("argv"))]
        return cpp_function(cpp_int(), "main", [], main_args, self.main_body())

    def main_body(self):
        task_registration = [self.set_top_level_task()] + self.register_tasks()
        mapper_registration = [self.set_default_mapper()]
        run_call = [cpp_var("return HighLevelRuntime::start(argc, argv)")]
        return task_registration + mapper_registration + run_call

    def set_top_level_task(self):
        return cpp_funcall("HighLevelRuntime::set_top_level_task_id", [],
                           [cpp_var(self.top_level_task.id())])

    def set_default_mapper(self):
        return cpp_funcall("HighLevelRuntime::set_registration_callback", [],
                           [cpp_var("register_random_mappers")])

    def register_tasks(self):
        code = []
        code += self.top_level_task.registration_code()
        for task in self.top_level_task.collect_tasks():
            code += task.registration_code()
        return code

    def pretty_string(self):
        boilerplate = [cpp_include("legion.h"),
                       cpp_include("random_mapper.h"),
                       cpp_using("LegionRuntime::HighLevel"),
                       cpp_using("LegionRuntime::Accessor"),
                       cpp_using("LegionRuntime::Arrays"),
                       self.scope_struct(),
                       self.pretty_task_id_enum()] + self.pretty_field_id_enums()
        return cpp_top_level_items(boilerplate +
                                   self.pretty_task_functions() +
                                   [self.pretty_main()])

    def scope_struct(self):
        all_regions = self.collect_all_regions()
        # all_partitions = self.collect_all_partitions()
        # partition_declarations = [ "LogicalPartition " + p.name for p in all_partitions]
        region_declarations = [ "LogicalRegion " + r.name for r in all_regions]
        # member_declarations = region_declarations + partition_declarations
        return cpp_struct("LogicalRegionsAndPartitions", region_declarations)

    def collect_all_regions(self):
        all_tasks = self.top_level_task.collect_tasks()
        regions = flatten([task.logical_regions_created for task in all_tasks])
        sub_regions = flatten([region.collect_subregions() for region in regions])
        return regions + sub_regions
