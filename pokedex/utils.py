from __future__ import unicode_literals

from prompt_toolkit.shortcuts import create_prompt_application
from prompt_toolkit.key_binding.registry import Registry
from prompt_toolkit.shortcuts import run_application
from termcolor import colored
import binascii, os, yaml
from pprint import pprint

def load_config(config_file):
    if os.path.isfile(os.path.realpath(config_file)):
        with open(os.path.realpath(config_file), 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as exc:
                pass

    raise IOError('Could not read %s.' % os.path.realpath(config_file))


def intro():
    print(red('I wanna be the very best,'))
    print(red('Like no one ever was.'))
    print(white('To catch them is my real test,'))
    print(white('To train them is my cause.'))
    print('')

def white(msg):
    return colored(msg, 'white', attrs=['bold'])

def red(msg, **kwargs):
    return colored(msg, 'red', **kwargs)

