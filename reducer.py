from copy import *
from datetime import datetime
from os.path import *
from random import *

from task import *
from test_case import *
from test_suite import *

max_reductions = 100

#failing case that does not have a read before write error: /Users/dillon/PythonWorkspace/test_gen/suites/reduction_test_2015_10_28_16_39_52/test_1_4
#another: ~/PythonWorkspace/test_gen/suites/reduction_test_2015_10_28_16_42_50/test_1_99/
#yet another: ~/PythonWorkspace/test_gen/suites/reduction_test_2015_10_28_16_51_48/test_1_198/
# and another: /Users/dillon/PythonWorkspace/test_gen/suites/reduction_test_2015_10_28_17_04_21/test_1_296

def reduce_failed_test(test_dir, failing_case, original_fail_result):
    suite_dir = "reduction_test_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    mkdir(join(test_dir, suite_dir))
    fail_case_stack = [failing_case]
    num_reductions = 0
    while num_reductions < max_reductions:
        last_failing_case = fail_case_stack[len(fail_case_stack) - 1]
        next_case = copy_with_random_reduction(last_failing_case)
        test_name = next_case.name + '_' + str(num_reductions)
        test_loc = join(test_dir, suite_dir, test_name)
        run_res = run_test(test_loc, next_case)
        if same_result(run_res, original_fail_result):
#        if same_test_info(run_res, original_fail_result):
            print 'APPENDING NEW FAILED TEST:', test_name
            print run_res
            fail_case_stack.append(next_case)
        num_reductions += 1
    return fail_case_stack[len(fail_case_stack) - 1]

def copy_with_random_reduction(failing_case):
    new_case = deepcopy(failing_case)
    i = randint(0, 100)
    if i > 50:
        delete_leaf_task(new_case.top_level_task)
    elif i > 30:
        delete_field_from_region_requirement(new_case.top_level_task)
    else:
        delete_rr_with_one_field(new_case.top_level_task)
    return new_case

def delete_leaf_task(task):
    delete_random_leaf(task)
    task.shouldnt_print_anything()
    task.decide_what_should_print()

def delete_random_leaf(task):
    if task.child_tasks != []:
        leaf_children = filter(lambda t: t.child_tasks == [], task.child_tasks)
        non_leaf_children = filter(lambda t: not t in leaf_children, task.child_tasks)
        if leaf_children != []:
            leaf_children.pop(randint(0, len(leaf_children) - 1))
            task.child_tasks = leaf_children + non_leaf_children
        elif non_leaf_children != []:
            next_node = non_leaf_children[randint(0, len(non_leaf_children) - 1)]
            delete_random_leaf(next_node)

def delete_field_from_region_requirement(task):
    all_tasks = task.collect_tasks()
    all_rrs = list(chain(*map(lambda t: t.region_requirements, all_tasks)))
    legal_rrs = filter(lambda rr: len(rr.fields) > 1, all_rrs)
    if legal_rrs != []:
        rr_to_delete_from = legal_rrs[randint(0, len(legal_rrs) - 1)]
        fields = rr_to_delete_from.fields
        ind = randint(0, len(fields) - 1)
        print 'DELETING FIELD', fields[ind]
        fields.pop(ind)

def delete_rr_with_one_field(task):
    delete_one_field_rr(task)
    task.shouldnt_print_anything()
    task.decide_what_should_print()
    return task

def delete_one_field_rr(task):
    all_tasks = task.collect_tasks()
    all_tasks_to_delete_from = filter(lambda t: has_rr_with_one_field(t), all_tasks)
    if len(all_tasks_to_delete_from) == 0:
        return task
    i = randint(0, len(all_tasks_to_delete_from) - 1)
    selected_task = all_tasks_to_delete_from[i]
    delete_first_rr_with_one_field(selected_task)
    
def has_rr_with_one_field(task):
    return len(filter(lambda rr: len(rr.fields) == 1, task.region_requirements)) > 0

def delete_first_rr_with_one_field(task):
    i = 0
    for rr in task.region_requirements:
        if len(rr.fields) == 1:
            task.region_requirements.pop(i)
            break
        i += 1
    return
