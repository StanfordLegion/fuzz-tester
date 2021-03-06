from datetime import datetime

from reducer.linear import *
from test_generator import *
from test_suite import *

import os
test_dir = os.environ.get('TEST_DIR', os.getcwd() + "/tests")

def main():
    settings = TestGeneratorSettings()
    settings.seed = 134230
    settings.num_cases = 1
    depth = 2
    settings.max_region_requirements_per_task = depth
    settings.max_new_trees_per_task = depth
    settings.max_task_children = depth
    settings.max_depth = depth
    settings.max_task_tree_depth = depth
    # REduction privileges for + - /
    # mixed
    # index space launches
    settings.privileges = ['READ_WRITE']#, 'READ_ONLY']
    settings.coherences = ['EXCLUSIVE'] #, 'ATOMIC', 'SIMULTANEOUS'] #, 'ATOMIC', '
    settings.runner = [] #"mpirun --host n0001,n0002,n0003,n0000 -np 4 --bind-to none -x GASNET_BACKTRACE=1"
    settings.legion_spy_flags = ["-level", "legion_spy=2"]
    run_timestamped_test_suite(settings)
    # run_and_reduce_timestamped_test_suite(settings)
    # run_case("/Users/ludwig/Code/fuzz-tester/tests/test_2016_02_04_20_55_07/test_0", "test_0")
    # run_legion_spy("/Users/ludwig/Code/fuzz-tester/tests/test_2016_02_04_20_55_07/test_0", "test_0")
    # run_test_suite("/Users/ludwig/Code/fuzz-tester/tests", "test_2016_02_04_20_55_07/test_0", ["test_0"])

def run_and_reduce_timestamped_test_suite(settings):
    suite_dir = "test_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    cases = generate_random_cases(settings)
    results = run_test_suite(test_dir, suite_dir, cases, settings)
    reduce_failing_case(cases, results)

def reduce_failing_case(cases, results):
    failed_tests = filter(lambda c: test_failed(results[c.name]), cases)
    if len(failed_tests) == 0:
        process_and_print_results(results)
    else:
        fail_func = lambda r: r.result_str == results[failed_tests[0].name].result_str
        new_case = reduce_failed_test(test_dir, failed_tests[0], fail_func)

def run_timestamped_test_suite(settings):
    suite_dir = "test_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    cases = generate_random_cases(settings)
    results = run_test_suite(test_dir, suite_dir, cases, settings)
    process_and_print_results(results)

def process_and_print_results(results):
    all_passed = True
    result_str = ''
    num_cases = 0
    num_failed = 0
    for case in results:
        num_cases += 1
        if test_failed(results[case]):
            result_str += case + '\tFAILED\t' + results[case].to_string() + '\n'
            all_passed = False
            num_failed += 1
    if all_passed:
        result_str = 'All tests passed'
    print_results(result_str, num_cases, num_failed)

def print_results(result_str, num_cases, num_failed):
    print ''
    print '========================== TEST RESULTS ========================='
    print ''
    print '--------------------------- SUMMARY -----------------------------'
    print 'Cases:         ' + str(num_cases)
    print 'Succeeded:     ' + str(num_cases - num_failed)
    print 'Failed:        ' + str(num_failed)
    print ''
    print '--------------------------- FAILURES ----------------------------'
    print ''
    print result_str
    print '================================================================='
    if num_failed != 0:
        exit(num_failed)
    else:
        exit(0)

if __name__ == "__main__":
    main()
