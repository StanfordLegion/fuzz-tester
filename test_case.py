from itertools import chain

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
        run_call = cpp_var("return HighLevelRuntime::start(argc, argv)")
        return task_registration + [run_call]

    def set_top_level_task(self):
        return cpp_funcall("HighLevelRuntime::set_top_level_task_id", [],
                           [cpp_var(self.top_level_task.id())])

    def register_tasks(self):
        code = []
        code += self.top_level_task.registration_code()
        for task in self.top_level_task.collect_tasks():
            code += task.registration_code()
        return code

    def pretty_string(self):
        boilerplate = [cpp_include("legion.h"),
                       cpp_using("LegionRuntime::HighLevel"),
                       cpp_using("LegionRuntime::Accessor"),
                       self.boilerplate_scope_struct(),
                       self.pretty_task_id_enum()] + self.pretty_field_id_enums()
        return cpp_top_level_items(boilerplate +
                                   self.pretty_task_functions() +
                                   [self.pretty_main()])
    def boilerplate_scope_struct(self):
        return \
'''
//==========================================================================
//                    LogicalRegionsAndPartitions
//==========================================================================

#include <string>
#include <map>
using namespace std;

struct LogicalRegionsAndPartitions {
public:
    map<string, LogicalRegion>    logical_regions;
    map<string, LogicalPartition> logical_partitions;
};

//==========================================================================
//                  Preserving your scope since 2016
//==========================================================================
'''
