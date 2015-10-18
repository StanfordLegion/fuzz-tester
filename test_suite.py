from os import mkdir
from os.path import *

from subprocess import *

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
    return run_case(test_location)

def create_test_dir(test_location, test_case):
    mkdir(test_location)
    src_file = open(join(test_location, test_case.name + '.cc'), 'w+')
    src_file.write(test_case.pretty_string())
    makefile = open(join(test_location, "Makefile"), 'w+')
    makefile.write(makefile_string(test_case.name))

def makefile_string(file_name):
    return 'ifndef LG_RT_DIR\n$(error LG_RT_DIR variable is not defined, aborting build)\nendif\nDEBUG=1\nOUTPUT_LEVEL=LEVEL_DEBUG\nSHARED_LOWLEVEL=1\nCC_FLAGS=-DLEGION_SPY\nOUTFILE\t:= ' + file_name + '\nGEN_SRC\t:= ' + file_name + '.cc' + '\ninclude $(LG_RT_DIR)/runtime.mk\n'

def compile_case(test_dir):
    build_process = Popen('make -j4 -C ' + test_dir, shell=True, )
    build_process.communicate()
    return build_process.returncode

def run_case(test_dir):
    return 0
