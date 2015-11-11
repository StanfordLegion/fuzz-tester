from datetime import datetime
from os import *
from os.path import *

def reduce_failed_test(test_dir, failing_case, original_fail_result):
    create_reduction_dir(test_dir)
    fail_case = failing_case
    fail_case = reduce_task_tree(fail_case, original_fail_result)
    fail_case = reduce_region_requirements(fail_case, original_fail_result)
    fail_case = reduce_region_requirement_fields(fail_case, original_fail_result)
    
def create_reduction_dir(test_dir):
    suite_dir = "reduction_test_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    mkdir(join(test_dir, suite_dir))    

def reduce_task_tree(fail_case, original_fail_result):
    return fail_case

def reduce_region_requirements(fail_case, original_fail_result):
    return fail_case

def reduce_region_requirement_fields(fail_case, original_fail_result):
    return fail_case
