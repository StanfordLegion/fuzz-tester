from os import makedirs
from os.path import *
from shutil import copyfile

from legion_spy_parser import *
from subprocess import *
from test_result import *

import os

legion_path = os.environ['LG_RT_DIR']
legion_spy_path = os.environ.get('LEGION_SPY_PATH', join(legion_path, '..', 'tools', 'legion_spy.py'))

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
    return success()
    # return parse_spy_output(test_location)

def create_test_dir(test_location, test_case):
    makedirs(test_location)
    src_file = open(join(test_location, test_case.name + '.cc'), 'w+')
    src_file.write(test_case.pretty_string())
    makefile = open(join(test_location, "Makefile"), 'w+')
    makefile.write(makefile_string(test_case.name))
    copyfile(join("template", "random_mapper.h"),  join(test_location, "random_mapper.h"))
    copyfile(join("template", "random_mapper.cc"), join(test_location, "random_mapper.cc"))

def makefile_string(file_name):
    return '''
ifndef LG_RT_DIR
  $(error LG_RT_DIR variable is not defined, aborting build)
endif
DEBUG ?= 1
OUTPUT_LEVEL ?= LEVEL_DEBUG
SHARED_LOWLEVEL ?= 0
USE_CUDA ?= 0
USE_GASNET ?= 0
CC_FLAGS ?= -std=c++11 -DLEGION_SPY
OUTFILE := %s
GEN_SRC := %s.cc random_mapper.cc
include $(LG_RT_DIR)/runtime.mk
''' % (file_name, file_name)

def compile_case(test_dir):
    threads = os.environ.get('THREADS', '4')
    build_process = Popen(['make', '-j', threads, '-C', test_dir])
    build_process.communicate()
    if build_process.returncode == 0:
        return success()
    else:
        return build_failed('build error code ' + str(build_process.returncode))

def run_case(test_location, test_name, settings):
    runner = settings.runner
    test_executable_path = join(test_location, test_name)
    log_files_template = join(test_location, "spy.log")
    command = runner + [test_executable_path] + settings.legion_spy_flags + ['-logfile', log_files_template]
    run_process = Popen(command)
    run_process.communicate()
    if run_process.returncode == 0:
        return success()
    else:
        return run_failed('run error code ' + str(run_process.returncode))

def run_legion_spy(test_location, test_name):
    spy_log_file = join(test_location, 'spy.log')
    spy_output_file = join(test_location, 'spy_results.txt')
    spy_options = ' -lpa '
    run_legion_spy_command_string = legion_spy_path + spy_options + spy_log_file + ' > ' + spy_output_file
    spy_process = Popen(run_legion_spy_command_string, shell=True, stdout=PIPE)
    spy_process.communicate()
    if spy_process.returncode == 0:
        return success()
    else:
        return legion_spy_failed('legion spy error code ' + str(spy_process.returncode))
