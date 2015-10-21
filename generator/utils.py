from random import randint

from generator.test_generator_settings import TestGeneratorSettings

def should_stop(depth, settings):
    i = randint(0, settings.stop_constant)
    return depth >= settings.max_depth or i == 0
