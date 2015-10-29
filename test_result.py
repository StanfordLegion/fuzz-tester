class TestRunInfo():
    def __init__(self, result, result_str):
        self.result = result
        self.passed = result == TestResult.SUCCESS
        self.result_str = result_str

    def to_string(self):
        return self.result_str

class TestResult():
    SUCCESS, BUILD_FAILED, RUN_FAILED, PARSE_FAILED, DEPENDENCE_ERRORS = range(5)

def same_result(l, r):
    return l.result == r.result

def same_test_info(l, r):
    return l.result == r.result and l.result_str == r.result_str

def build_failed(msg):
    return TestRunInfo(TestResult.BUILD_FAILED, msg)

def run_failed(msg):
    return TestRunInfo(TestResult.RUN_FAILED, msg)

def parse_failed(msg):
    return TestRunInfo(TestResult.PARSE_FAILED, msg)

def dependence_errors(msg):
    return TestRunInfo(TestResult.DEPENDENCE_ERRORS, msg)

def success():
    return TestRunInfo(TestResult.SUCCESS, '')

def test_failed(test_info):
    return not test_info.passed
