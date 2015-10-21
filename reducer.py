from copy import copy
from datetime import datetime
from os.path import *
from random import *

from task import *
from test_case import *
from test_suite import *

max_reductions = 5

def reduce_failed_test(test_dir, failing_case):
    suite_dir = "reduction_test_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    mkdir(join(test_dir, suite_dir))
    fail_case_stack = [failing_case]
    num_reductions = 0
    while num_reductions < max_reductions:
        last_failing_case = fail_case_stack[len(fail_case_stack) - 1]
        next_case = copy_with_random_leaf_task_deleted(last_failing_case)
        test_name = next_case.name + '_' + str(num_reductions)
        test_loc = join(test_dir, suite_dir, test_name)
        run_res = run_test(test_loc, next_case)
        if run_res != '':
            print 'FAILED'
            fail_case_stack.append(next_case)
        else:
            print 'MODIFIED CASE PASSED'
        num_reductions += 1
    return fail_case_stack[len(fail_case_stack) - 1]

def copy_with_random_leaf_task_deleted(failing_case):
    new_task_tree = copy_task_tree_with_deletion(failing_case.top_level_task)
    copy = TestCase(failing_case.name, new_task_tree)
    return copy

def copy_task_tree_with_deletion(task):
    copy_task = copy(task)
    if copy_task.child_tasks == []:
        return copy_task
    else:
        leaf_children = filter(lambda t: t.child_tasks == [], copy_task.child_tasks)
        non_leaf_childran = filter(lambda t: not t in leaf_children, copy_task.child_tasks)
        if leaf_children == []:
            return copy_task
        else:
            print 'about to remove, size', str(len(leaf_children))
            leaf_children.pop(randint(0, len(leaf_children) - 1))
            print 'leaf children size', str(len(leaf_children))
            copy_task.child_tasks = leaf_children
            print 'removed task, num tasks: ', str(len(copy_task.child_tasks))
            return copy_task
