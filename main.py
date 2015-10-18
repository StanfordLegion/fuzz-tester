from test_case import *
from test_suite import *

t = Task("top_level_task")
case = TestCase("tiny_test", t, [t])
suite_dir = "tiny_test_suite"
test_dir = "/Users/dillon/PythonWorkspace/test_gen/suites"

results = run_test_suite(test_dir, suite_dir, [case])

print ''
print '-------------------------- TEST RESULTS -------------------------'

all_passed = True
for case in results:
    if results[case] != 0:
        print case, 'FAILED, error code:', results[case]
        all_passed = False

if all_passed:
    print 'All tests passed'

print '-----------------------------------------------------------------'
