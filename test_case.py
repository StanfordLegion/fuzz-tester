from cpp_code import *

def run_test_case(case):
    print case.pretty_string()

class TestCase():

    def __init__(self, name, top_level_task, all_tasks):
        self.name = name
        self.top_level_task = top_level_task
        self.tasks = all_tasks

    def pretty_task_id_enum(self):
        return cpp_enum("FIELD_ID", [])

    def pretty_field_id_enum(self):
        task_id_names = []
        for task in self.tasks:
            task_id_names.append(task.id())
        return cpp_enum("TASK_ID", task_id_names)

    def pretty_task_functions(self):
        task_functions = []
        for task in self.tasks:
            task_functions.append(task.task_function())
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
        taskCode = []
        for task in self.tasks:
            taskCode.append(task.registration_code())
        return taskCode

    def pretty_string(self):
        boilerplate = [cpp_include("legion.h"),
                       cpp_using("LegionRuntime::HighLevel"),
                       cpp_using("LegionRuntime::Accessor"),
                       self.pretty_task_id_enum(),
                       self.pretty_field_id_enum()]
        return cpp_top_level_items(boilerplate +
                                   self.pretty_task_functions() + 
                                   [self.pretty_main()])

class Task():
    def __init__(self, name):
        self.name = name

    def task_function(self):
        runtime = cpp_formal_param(cpp_ptr(cpp_var("HighLevelRuntime")), cpp_var("runtime"))
        context = cpp_formal_param(cpp_var("Context"), cpp_var("ctx"))
        regions = cpp_formal_param(cpp_const(cpp_ref(cpp_var("std::vector<PhysicalRegion>"))), cpp_var("regions"))
        task = cpp_formal_param(cpp_const(cpp_ptr(cpp_var("Task"))), cpp_var("task"))
        task_args = [task, regions, context, runtime]
        return cpp_function(cpp_void(), self.name, [], task_args, [])

    def registration_code(self):
        args = [cpp_var(self.id()),
                cpp_var("Processor::LOC_PROC"),
                cpp_var("true"),
                cpp_var("false")]
        return cpp_funcall("HighLevelRuntime::register_legion_task", [self.name], args)

    def id(self):
        return self.name.upper() + "_ID"
