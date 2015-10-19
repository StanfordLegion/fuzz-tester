from test_generator import *
from test_suite import *

settings = TestGeneratorSettings()
suite_dir = "tiny_test_suite"
test_dir = "/Users/dillon/PythonWorkspace/test_gen/suites"
cases = generate_random_cases(settings)

results = run_test_suite(test_dir, suite_dir, cases)

print ''
print '-------------------------- TEST RESULTS -------------------------'

all_passed = True
result_str = ''
num_cases = 0
for case in results:
    num_cases += 1
    if results[case] != '':
        result_str += case + '\tFAILED\t' + results[case] + '\n'
        all_passed = False
        
if all_passed:
    result_str = 'All tests passed'

print 'Cases:\t' + str(num_cases)
print result_str

print '-----------------------------------------------------------------'
