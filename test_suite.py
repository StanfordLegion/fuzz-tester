from os import mkdir
from os.path import *

from subprocess import *

legion_spy_path = '/Users/dillon/CppWorkspace/Legion/Master/legion/tools/legion_spy.py'

def run_test_suite(test_dir, suite_dir, cases):
    test_results = {}
    mkdir(join(test_dir, suite_dir))
    for test_case in cases:
        test_location = join(test_dir, suite_dir, test_case.name)
        test_result = run_test(test_location, test_case)
        test_results[test_case.name] = test_result
    return test_results

def run_test(test_location, test_case):
    create_test_dir(test_location, test_case)
    compile_res = compile_case(test_location)
    if compile_res != 0:
        return compile_res
    run_res = run_case(test_location, test_case.name)
    if run_res != 0:
        return run_res
    return run_legion_spy(test_location, test_case.name)

def create_test_dir(test_location, test_case):
    mkdir(test_location)
    src_file = open(join(test_location, test_case.name + '.cc'), 'w+')
    src_file.write(test_case.pretty_string())
    makefile = open(join(test_location, "Makefile"), 'w+')
    makefile.write(makefile_string(test_case.name))

def makefile_string(file_name):
    return 'ifndef LG_RT_DIR\n$(error LG_RT_DIR variable is not defined, aborting build)\nendif\nDEBUG=1\nOUTPUT_LEVEL=LEVEL_DEBUG\nSHARED_LOWLEVEL=1\nCC_FLAGS=-DLEGION_SPY\nOUTFILE\t:= ' + file_name + '\nGEN_SRC\t:= ' + file_name + '.cc' + '\ninclude $(LG_RT_DIR)/runtime.mk\n'

def compile_case(test_dir):
    build_process = Popen('make -j4 -C ' + test_dir, shell=True)
    build_process.communicate()
    return build_process.returncode

def run_case(test_location, test_name):
    spy_log_file = join(test_location, "spy.log")
    test_executable_path = join(test_location, test_name)
    legion_spy_flags = " -level 2 -cat legion_spy -logfile " + spy_log_file
    run_command_string = test_executable_path + legion_spy_flags
    run_process = Popen(run_command_string, shell=True)
    run_process.communicate()
    return run_process.returncode

def run_legion_spy(test_location, test_name):
    spy_log_file = join(test_location, "spy.log")
    spy_options = ' -l '
    run_legion_spy_command_string = legion_spy_path + spy_options + spy_log_file
    spy_process = Popen(run_legion_spy_command_string, shell=True)
    spy_process.communicate()
    return spy_process.returncode
