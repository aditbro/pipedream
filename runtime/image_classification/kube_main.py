import os
import sys

arg_list = os.getenv('arg_list')
args_str = ''

for arg in arg_list.split(' ')[:-1]:
    arg_val = arg.replace('Q', '-')
    args_str += ' {} {} '.format(arg_val, os.getenv(arg))

os.system('python -u main_with_runtime.py {}'.format(args_str))

