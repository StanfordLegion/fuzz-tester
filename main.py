from datetime import datetime

from reducer.hierarchical import *
from test_generator import *
from test_suite import *

test_dir = "/Users/dillon/PythonWorkspace/test_gen/suites"

def main():
    settings = TestGeneratorSettings()
    settings.seed = 134221
    settings.num_cases = 1
    settings.max_new_trees_per_task = 1
    settings.max_task_children = 100
    settings.max_depth = 1
    settings.max_task_tree_depth = 1
    settings.privileges = ['READ_WRITE']
    run_timestamped_test_suite(settings)
#    run_and_reduce_timestamped_test_suite(settings)

def run_and_reduce_timestamped_test_suite(settings):
    suite_dir = "test_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    cases = generate_random_cases(settings)
    results = run_test_suite(test_dir, suite_dir, cases)
    failed_tests = filter(lambda c: test_failed(results[c.name]), cases)
    if len(failed_tests) == 0:
        process_and_print_results(results)
    else:
        new_case = reduce_failed_test(test_dir, failed_tests[0], results[failed_tests[0].name])
    
def run_timestamped_test_suite(settings):
    suite_dir = "test_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    cases = generate_random_cases(settings)
    results = run_test_suite(test_dir, suite_dir, cases)
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

if __name__ == "__main__":
    main()
