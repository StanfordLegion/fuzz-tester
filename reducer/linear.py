from datetime import datetime
from os.path import *
from os import makedirs

from reducer.actions import *
from task import *
from test_case import *
from test_suite import *

max_reductions = 300

# failing, but with warnings: ~/PythonWorkspace/test_gen/suites/reduction_test_2015_10_29_18_18_01/test_0_98/
# failing, no warnings: ~/PythonWorkspace/test_gen/suites/reduction_test_2015_10_29_18_27_06/test_0_176/ NOTE: This looks like a dynamic test of disjointness issue, wasnt this already resolved?

def reduce_failed_test(test_dir, failing_case, fail_func): #original_fail_result):
    suite_dir = "reduction_test_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    makedirs(join(test_dir, suite_dir))
    fail_case_stack = [failing_case]
    num_reductions = 0
    while num_reductions < max_reductions:
        last_failing_case = fail_case_stack[len(fail_case_stack) - 1]
        next_case = copy_with_random_reduction(last_failing_case)
        test_name = next_case.name + '_' + str(num_reductions)
        test_loc = join(test_dir, suite_dir, test_name)
        run_res = run_test(test_loc, next_case)
        if fail_func(run_res): #same_result(run_res, original_fail_result):
            print 'APPENDING NEW FAILED TEST:', test_name
            print run_res
            fail_case_stack.append(next_case)
        num_reductions += 1
    return fail_case_stack[len(fail_case_stack) - 1]
