from test_generator import *
from test_suite import *

settings = TestGeneratorSettings()
suite_dir = "tests_10_19_2015"
test_dir = "/Users/dillon/PythonWorkspace/test_gen/suites"
cases = generate_random_cases(settings)

results = run_test_suite(test_dir, suite_dir, cases)

print ''
print '========================== TEST RESULTS ========================='

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

print ''
print '--------------------------- SUMMARY -----------------------------'
print 'Cases:         ' + str(num_cases)
print 'Succeeded:     ' + str(num_cases - num_failed)
print 'Failed:        ' + str(num_failed)
print ''
print '--------------------------- FAILURES ----------------------------'
print''
print result_str
print '================================================================='
