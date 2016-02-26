from os import makedirs
from os.path import *
from shutil import copyfile

from legion_spy_parser import *
from subprocess import *
from test_result import *

import os

legion_path = os.environ['LG_RT_DIR']
legion_spy_path = os.environ.get('LEGION_SPY_PATH', join(legion_path, 'tools', 'legion_spy.py'))

def run_test_suite(test_dir, suite_dir, cases, settings):
    test_results = {}
    makedirs(join(test_dir, suite_dir))
    for test_case in cases:
        test_location = join(test_dir, suite_dir, test_case.name)
        test_result = run_test(test_location, test_case, settings)
        test_results[test_case.name] = test_result
    return test_results

def run_test(test_location, test_case, settings):
    create_test_dir(test_location, test_case)
    compile_res = compile_case(test_location)
    if test_failed(compile_res):
        return compile_res
    run_res = run_case(test_location, test_case.name, settings)
    if test_failed(run_res):
        return run_res
    run_spy_res = run_legion_spy(test_location, test_case.name)
    if test_failed(run_spy_res):
        return run_spy_res
    return parse_spy_output(test_location)

def create_test_dir(test_location, test_case):
    makedirs(test_location)
    src_file = open(join(test_location, test_case.name + '.cc'), 'w+')
    src_file.write(test_case.pretty_string())
    makefile = open(join(test_location, "Makefile"), 'w+')
    makefile.write(makefile_string(test_case.name))
    copyfile(join("template", "random_mapper.h"),  join(test_location, "random_mapper.h"))
    copyfile(join("template", "random_mapper.cc"), join(test_location, "random_mapper.cc"))

def makefile_string(file_name):
    return 'ifndef LG_RT_DIR\n$(error LG_RT_DIR variable is not defined, aborting build)\nendif\nDEBUG=1\nOUTPUT_LEVEL=LEVEL_DEBUG\nSHARED_LOWLEVEL=0\nUSE_CUDA=0\nUSE_GASNET=0\nCC_FLAGS=-DLEGION_SPY\nOUTFILE\t:= ' + file_name + '\nGEN_SRC\t:= ' + file_name + '.cc random_mapper.cc' + '\ninclude $(LG_RT_DIR)/runtime.mk\n'

def compile_case(test_dir):
    build_process = Popen('make -j4 -C ' + test_dir, shell=True)
    build_process.communicate()
    if build_process.returncode == 0:
        return success()
    else:
        return build_failed('build error code ' + str(build_process.returncode))

def run_case(test_location, test_name, settings):
    runner = settings.runner
    spy_log_file = join(test_location, "spy.log")
    test_executable_path = join(test_location, test_name)
    legion_spy_flags = " -level 2 -cat legion_spy -logfile " + spy_log_file
    run_command_string = runner + ' ' + test_executable_path + legion_spy_flags
    run_process = Popen(run_command_string, shell=True)
    run_process.communicate()
    if run_process.returncode == 0:
        return success()
    else:
        return run_failed('run error code ' + str(run_process.returncode))

def run_legion_spy(test_location, test_name):
    spy_log_file = join(test_location, 'spy.log')
    spy_output_file = join(test_location, 'spy_results.txt')
    spy_options = ' -l '
    run_legion_spy_command_string = legion_spy_path + spy_options + spy_log_file + ' > ' + spy_output_file
    spy_process = Popen(run_legion_spy_command_string, shell=True, stdout=PIPE)
    spy_process.communicate()
    if spy_process.returncode == 0:
        return success()
    else:
        return legion_spy_failed('legion spy error code ' + str(spy_process.returncode))
