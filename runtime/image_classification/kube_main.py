import os

arg_list = os.getenv('args_list')
args_str = ''

for arg in arg_list:
    arg_val = arg.replace('Q', '-')
    args_str += ' {} {} '.format(arg_val, os.getenv(arg))

print('python main_with_runtime.py {}'.format(args_str))

os.system('python main_with_runtime.py {}'.format(args_str))

