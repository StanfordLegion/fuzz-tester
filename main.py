from datetime import datetime

from test_generator import *
from test_suite import *

test_dir = "/Users/dillon/PythonWorkspace/test_gen/suites"

def main():
    settings = TestGeneratorSettings()
    settings.seed = 100
    run_timestamped_test_suite(settings)

def run_timestamped_test_suite(settings):
    suite_dir = "test_" + datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
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
        if results[case] != '':
            result_str += case + '\tFAILED\t' + results[case] + '\n'
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

main()
