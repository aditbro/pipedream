import os

arg_list = os.getenv('arg_list')
args_str = ''

for arg in arg_list.split(' ')[:-1]:
    arg_val = arg.replace('Q', '-')
    args_str += ' {} {} '.format(arg_val, os.getenv(arg))

print('python main_with_runtime.py {} &> /home/aditya/ta_log/test'.format(args_str))

os.system('python main_with_runtime.py {}'.format(args_str))

