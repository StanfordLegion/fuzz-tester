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
        return parse_dep_error_line(dep_lines[0])

def parse_dep_error_line(dep_line):
    dep_errors = int(search('(.+): ([0-9]+)', dep_line).group(2))
    if dep_errors == 0:
        return success()
    else:
        return dependence_errors('dependence errors: ' + str(dep_errors))
