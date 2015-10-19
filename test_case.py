from itertools import chain

from cpp_code import *

def run_test_case(case):
    print case.pretty_string()

class TestCase():
    def __init__(self, name, top_level_task):
        self.name = name
        self.top_level_task = top_level_task

    def pretty_field_id_enums(self):
        all_field_spaces = self.top_level_task.collect_field_spaces()
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
        return [self.set_top_level_task()] + self.register_tasks()

    def set_top_level_task(self):
        return cpp_funcall("HighLevelRuntime::set_top_level_task_id", [],
                           [cpp_var(self.top_level_task.id())])

    def register_tasks(self):
        taskCode = [self.top_level_task.registration_code()]
        return map(lambda t: t.registration_code(), self.top_level_task.collect_tasks())

    def pretty_string(self):
        boilerplate = [cpp_include("legion.h"),
                       cpp_using("LegionRuntime::HighLevel"),
                       cpp_using("LegionRuntime::Accessor"),
                       self.pretty_task_id_enum()] + self.pretty_field_id_enums()
        return cpp_top_level_items(boilerplate +
                                   self.pretty_task_functions() + 
                                   [self.pretty_main()])

# Task argument boilerplate
runtime = cpp_formal_param(cpp_ptr(cpp_var("HighLevelRuntime")), cpp_var("runtime"))
context = cpp_formal_param(cpp_var("Context"), cpp_var("ctx"))
regions = cpp_formal_param(cpp_const(cpp_ref(cpp_var("std::vector<PhysicalRegion>"))), cpp_var("regions"))
task = cpp_formal_param(cpp_const(cpp_ptr(cpp_var("Task"))), cpp_var("task"))
task_args = [task, regions, context, runtime]

class Task():
    def __init__(self, name, region_requirements):
        self.name = name
        self.logical_regions_created = []
        self.region_requirements = region_requirements
        self.child_tasks = []

    def collect_field_spaces(self):
        return map(lambda x: x.field_space, self.logical_regions_created)

    def collect_tasks(self):
        all_tasks = [self]
        for child in self.child_tasks:
            all_tasks += child.collect_tasks()
        return all_tasks        

    def index_spaces_init(self):
        index_spaces = map(lambda x: x.index_space, self.logical_regions_created)
        index_spaces_to_init = filter(lambda i: i.task_name == self.name, index_spaces)
        return map(lambda i: i.init_code(), index_spaces_to_init)

    def field_spaces_init(self):
        field_spaces = map(lambda x: x.field_space, self.logical_regions_created)
        field_spaces_to_init = filter(lambda fs: fs.task_name == self.name, field_spaces)
        init_code_lists = map(lambda fs: fs.init_code(), field_spaces_to_init)
        init_code = []
        for i in init_code_lists:
            init_code.extend(i)
        return init_code

    def logical_regions_created_init(self):
        return map(lambda lr: lr.init_code(), self.logical_regions_created)

    def logical_regions_init(self):
        return self.index_spaces_init() + self.field_spaces_init() + self.logical_regions_created_init()

    def region_requirements_code(self, launcher_name):
        rr_code = []
        i = 0
        for rr in self.region_requirements:
            rr_code.extend(rr.init_code(i, launcher_name))
            i += 1
        return rr_code

    def launch_code(self):
        launcher_name = self.name + '_launcher'
        null_arg = cpp_var('TaskArgument(NULL, 0)')
        launcher_init = cpp_funcall('TaskLauncher ' + launcher_name, [], [self.id(), null_arg])
        launch_call = cpp_funcall('runtime->execute_task', [], ['ctx', launcher_name])
        return [launcher_init] + self.region_requirements_code(launcher_name) + [launch_call]

    def child_task_launches(self):
        launches = []
        for child_task in self.child_tasks:
            launches.extend(child_task.launch_code())
        return launches
    
    def task_function(self):
        task_body = self.logical_regions_init() + self.child_task_launches()
        return cpp_function(cpp_void(), self.name, [], task_args, task_body)

    def registration_code(self):
        args = [cpp_var(self.id()),
                cpp_var("Processor::LOC_PROC"),
                cpp_var("true"),
                cpp_var("false")]
        return cpp_funcall("HighLevelRuntime::register_legion_task", [self.name], args)

    def id(self):
        return self.name.upper() + "_ID"
