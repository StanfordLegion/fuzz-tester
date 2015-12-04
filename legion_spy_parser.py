from os.path import *
from re import search

from test_result import *

def parse_spy_output(test_location):
    spy_result_str = open(join(test_location, 'spy_results.txt')).read()
    return parse_spy_str(spy_result_str)

def parse_spy_str(result_str):
    result_str = result_str.replace('\r', '\n')
    lines_wo_leading_whitespace = map(lambda l: l.lstrip(), result_str.split('\n'))
    dep_lines = filter(lambda l: l.startswith('Mapping Dependence Errors:'), lines_wo_leading_whitespace)
    if len(dep_lines) == 0:
        return parse_failed('Could not find mapping dependence line')
    else:
        error_lines = parse_error_lines(lines_wo_leading_whitespace)
        err = parse_dep_error_line(dep_lines, error_lines)
        return err

def parse_error_lines(lines):
    return filter(lambda l: l.startswith('ERROR:'), lines)

def parse_dep_error_line(dep_lines, error_lines):
    dep_errors = map(lambda dep_line: int(search('(.+): ([0-9]+)', dep_line).group(2)), dep_lines)
    num_dep_errors = sum(dep_errors)
    close_lines = filter(lambda l: 'Close' in l, error_lines)
    num_close_errs = len(close_lines)
    if num_dep_errors == 0:
        return success()
    else:
        return dependence_errors('dependence errors: ' + str(dep_errors), num_dep_errors, num_close_errs)
