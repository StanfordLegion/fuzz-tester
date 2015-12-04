class TestRunInfo():
    def __init__(self, result, result_str, mapping_dep_errors, close_errors):
        self.result = result
        self.error_lines = []
        self.passed = result == TestResult.SUCCESS
        self.result_str = result_str
        self.mapping_dep_errors = mapping_dep_errors
        self.close_errors = close_errors

    def to_string(self):
        n = self.num_close_errors()
        if n > 0:
            return self.result_str + ', close errors: ' + str(n)
        else:
            return self.result_str

    def num_close_errors(self):
        return self.close_errors

    def num_non_close_dep_errors(self):
        r = self.mapping_dep_errors - self.num_close_errors()
        print str(r)
        print str(self.mapping_dep_errors)
        print str(self.num_close_errors())
        assert(r >= 0)
        return r

class TestResult():
    SUCCESS, BUILD_FAILED, RUN_FAILED, PARSE_FAILED, DEPENDENCE_ERRORS = range(5)

def same_result(l, r):
    return l.result == r.result

def same_test_info(l, r):
    return l.result == r.result and l.result_str == r.result_str

def build_failed(msg):
    return TestRunInfo(TestResult.BUILD_FAILED, msg, 0, 0)

def run_failed(msg):
    return TestRunInfo(TestResult.RUN_FAILED, msg, 0, 0)

def parse_failed(msg):
    return TestRunInfo(TestResult.PARSE_FAILED, msg, 0, 0)

def dependence_errors(msg, dep_errs, close_errs):
    return TestRunInfo(TestResult.DEPENDENCE_ERRORS, msg, dep_errs, close_errs)

def success():
    return TestRunInfo(TestResult.SUCCESS, '', 0, 0)

def test_failed(test_info):
    return not test_info.passed

def test_failed_no_close(test_info):
    return not test_info.passed and test_info.num_close_errors() == 0
