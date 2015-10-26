class TestRunInfo():
    def __init__(self, passed, result_str):
        self.passed = passed
        self.result_str = result_str

    def to_string(self):
        return self.result_str

def test_failed(test_info):
    return not test_info.passed
