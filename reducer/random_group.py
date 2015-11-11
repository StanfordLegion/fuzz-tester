from datetime import datetime
from os.path import *

from reducer.actions import *
from task import *
from test_case import *
from test_suite import *

SUCCESS_THRESHOLD = 15
MAX_REDUCTIONS_PER_GROUP = 1

def reduce_failed_test(test_dir, failing_case, original_fail_result):
    suite_dir = "reduction_test_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    mkdir(join(test_dir, suite_dir))
    fail_case_stack = [failing_case]
    consecutive_successes = 0
    num_reductions = 0
    while consecutive_successes < SUCCESS_THRESHOLD:
        last_failing_case = fail_case_stack[len(fail_case_stack) - 1]
        next_case = many_random_reductions(last_failing_case)
        test_name = next_case.name + '_' + str(num_reductions)
        test_loc = join(test_dir, suite_dir, test_name)
        run_res = run_test(test_loc, next_case)
        if same_result(run_res, original_fail_result):
            print 'APPENDING NEW FAILED TEST:', test_name
            print run_res.to_string()
            consecutive_successes = 0
            fail_case_stack.append(next_case)
        else:
            consecutive_successes += 1
        num_reductions += 1
    return fail_case_stack[len(fail_case_stack) - 1]

def many_random_reductions(failing_case):
    new_case = failing_case
    num_reductions = 0
    for i in xrange(0, randint(1, MAX_REDUCTIONS_PER_GROUP)):
        new_case = copy_with_random_reduction(new_case)
    return new_case
