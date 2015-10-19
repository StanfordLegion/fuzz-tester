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
        task_id_names = [self.top_level_task.id()]
        return cpp_enum("TASK_ID", task_id_names)

    def pretty_task_functions(self):
        task_functions = [self.top_level_task.task_function()]
        return task_functions

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
        return taskCode

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
    def __init__(self, name):
        self.name = name
        self.logical_regions_created = []

    def collect_field_spaces(self):
        return map(lambda x: x.field_space, self.logical_regions_created)

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
    
    def task_function(self):
        task_body = self.logical_regions_init()
        return cpp_function(cpp_void(), self.name, [], task_args, task_body)

    def registration_code(self):
        args = [cpp_var(self.id()),
                cpp_var("Processor::LOC_PROC"),
                cpp_var("true"),
                cpp_var("false")]
        return cpp_funcall("HighLevelRuntime::register_legion_task", [self.name], args)

    def id(self):
        return self.name.upper() + "_ID"
