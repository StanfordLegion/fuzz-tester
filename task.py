from itertools import chain

from cpp_code import *

class Task():
    def __init__(self, name, region_requirements, parent_region_requirements=[], is_index_task=False):
        self.name = name
        self.logical_regions_created = []
        self.region_requirements = set(region_requirements)
        self.parent_region_requirements = set(parent_region_requirements)
        self.child_tasks = []
        self.is_top_level = False
        self.is_index_task = is_index_task

    def all_field_spaces(self):
        return map(lambda rr: rr.region.field_space, self.region_requirements)

    def collect_field_spaces(self):
        all_field_spaces = map(lambda lr: lr.field_space, self.logical_regions_created)
        for child in self.child_tasks:
            all_field_spaces += child.collect_field_spaces()
        return all_field_spaces

    def collect_tasks(self):
        all_tasks = [self]
        for child in self.child_tasks:
            all_tasks += child.collect_tasks()
        return all_tasks

    def index_spaces_init(self):
        index_spaces = map(lambda x: x.index_space, self.logical_regions_created)
        index_spaces_to_init = filter(lambda i: i.task_name == self.name, index_spaces)
        return list(chain(*map(lambda i: i.init_code(), index_spaces_to_init)))

    def field_spaces_init(self):
        field_spaces = map(lambda x: x.field_space, self.logical_regions_created)
        field_spaces_to_init = filter(lambda fs: fs.task_name == self.name, field_spaces)
        init_code_lists = map(lambda fs: fs.init_code(), field_spaces_to_init)
        init_code = []
        for i in init_code_lists:
            init_code.extend(i)
        return init_code

    def logical_regions_created_init(self):
        return list(chain(*map(lambda lr: lr.init_code(self.name), self.logical_regions_created)))

    def logical_regions_init(self):
        code = []
        code += self.declare_scope()
        code += [cpp_comment("Initialise IndexSpaces")]
        code += self.index_spaces_init()
        code += [cpp_comment("Initialise FieldSpaces")]
        code += self.field_spaces_init()
        code += [cpp_comment("Create LogicalRegions")]
        code += self.logical_regions_created_init()
        if not self.is_top_level:
            code += self.retrieve_logical_regions()
        return code

    def declare_scope(self):
        code = []
        if self.is_top_level:
            code += ["LogicalRegionsAndPartitions scope"]
        elif len(self.all_logical_regions()) > 0:
            code += ["LogicalRegionsAndPartitions &scope = *( (LogicalRegionsAndPartitions*) task->args)"]
        return code


    def parent_logical_regions(self):
        regions  = set(rr.region for rr in self.region_requirements)
        parent_regions = set(rr.region for rr in self.parent_region_requirements)
        all_regions = regions.union(parent_regions)
        return all_regions.difference(self.logical_regions_created)

    def all_logical_regions(self):
        regions  = set(rr.region for rr in self.region_requirements)
        return regions.union(self.logical_regions_created)

    def retrieve_logical_regions(self):
        regions = self.parent_logical_regions()
        code = []
        if len(regions) > 0:
            code += [cpp_comment("Retrieve parents logical regions")]
        for r in regions:
            code += r.retrieve_code()
        return code

    def region_requirements_code(self, launcher_name):
        rr_code = []
        i = 0

        # Parent Region Requirements
        # Nope - we do not have requirements for the parents of these regions, so can't pass them along!
        # for rr in self.parent_region_requirements:
        #     rr_code.extend( rr.init_code(i, launcher_name) )
        #     i += 1

        # Own Region Requirements
        for rr in self.region_requirements:
            rr_code.extend(rr.init_code(i, launcher_name))
            i += 1
        return rr_code

    def launch_code(self):
        code = []
        code += [cpp_comment("Create TaskLauncher")]
        # code += ["serialized_scope = serialized_string(scope)"]
        launcher_name = self.name + '_index_launcher'
        argument = cpp_var('TaskArgument( &scope, sizeof(scope) )')
        if self.is_index_task:
            code += [cpp_comment("Create LaunchDomain")]
            arg_map_name = self.id() + "_argument_map"
            code += [cpp_var('ArgumentMap ' + arg_map_name)]
            launch_bounds_name = self.id() + "_launch_bounds"
            launch_bounds_decl = cpp_var('Rect<1> ' + launch_bounds_name)
            launch_bounds_creation = cpp_funcall("Rect", ["1"], ["Point<1>(0)", "Point<1>(5)"])
            code += [cpp_assign(launch_bounds_decl, launch_bounds_creation)]
            launch_domain_name = self.id() + "_launch_domain"
            launch_domain_decl = cpp_var('Domain ' + launch_domain_name)
            code += [cpp_assign(launch_domain_decl, launch_bounds_name)]
            launcher_init = cpp_funcall('IndexLauncher ' + launcher_name, [], [self.id(), launch_domain_name, argument, arg_map_name])
            execute_index_space = cpp_funcall('runtime->execute_index_space', [], ['ctx', launcher_name])
            future_map_name = self.id() + "future_map"
            future_map_decl = cpp_var('FutureMap ' + future_map_name)
            launch_call = [cpp_assign(future_map_decl, execute_index_space)]
            launch_call += [cpp_funcall(future_map_name + ".wait_all_results", [], [])]
        else:
            launcher_init = cpp_funcall('TaskLauncher ' + launcher_name, [], [self.id(), argument])
            launch_call = [cpp_funcall('runtime->execute_task', [], ['ctx', launcher_name])]
        code += [launcher_init]
        code += [cpp_funcall('runtime->attach_name', [], [cpp_var(self.id()), '"' + self.name + '"'])]
        code += self.region_requirements_code(launcher_name)
        code += launch_call
        return code

    def child_task_launches(self):
        launches = []
        for child_task in self.child_tasks:
            launches.extend(child_task.launch_code())
        return launches

    def report_run(self):
        string = self.id() + r" has completed!\n"
        return [cpp_funcall("printf", [], ['"' + string + '"'])]

    def task_function(self):
        task_body = self.logical_regions_init() + self.child_task_launches() + self.report_run()
        return cpp_function(cpp_void(), self.name, [], task_args, task_body)

    def registration_code(self):
        code = []
        single = "true" if not self.is_index_task else "false"
        index  = "true" if     self.is_index_task else "false"
        args = [cpp_var(self.id()),
                cpp_var("Processor::LOC_PROC"),
                cpp_var(single),
                cpp_var(index)]
        code += [cpp_funcall("Runtime::register_legion_task", [self.name], args)]
        return code

    def id(self):
        return self.name.upper() + "_ID"

    def should_print_region_requirements(self):
        map(lambda rr: rr.should_print(), self.region_requirements)

    def should_print_regions_created(self):
        map(lambda lr: lr.should_print_if_any_child_is_needed(), self.logical_regions_created)

    def decide_what_should_print(self):
        all_tasks = self.collect_tasks()
        map(lambda t: t.should_print_region_requirements(), all_tasks)
        map(lambda t: t.should_print_regions_created(), all_tasks)

    def shouldnt_print_regions(self):
        map(lambda lr: lr.shouldnt_print_anything(), self.logical_regions_created)

    def shouldnt_print_anything(self):
        map(lambda t: t.shouldnt_print_regions(), self.collect_tasks())

# Task argument boilerplate
runtime = cpp_formal_param(cpp_ptr(cpp_var("Runtime")), cpp_var("runtime"))
context = cpp_formal_param(cpp_var("Context"), cpp_var("ctx"))
regions = cpp_formal_param(cpp_const(cpp_ref(cpp_var("std::vector<PhysicalRegion>"))), cpp_var("regions"))
task = cpp_formal_param(cpp_const(cpp_ptr(cpp_var("Task"))), cpp_var("task"))
task_args = [task, regions, context, runtime]
