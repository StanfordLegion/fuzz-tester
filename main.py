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
for case in results:
    if results[case] != '':
        print case, '\tFAILED\t', results[case]
        all_passed = False

if all_passed:
    print 'All tests passed'

print '-----------------------------------------------------------------'
