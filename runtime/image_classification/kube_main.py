import subprocess
import os
import time

arg_list = os.getenv('arg_list')
args_str = ''

os.system('echo 0 > /workspace/healthcheck')

for arg in arg_list.split(' ')[:-1]:
    arg_val = arg.replace('Q', '-')
    args_str += ' {} {} '.format(arg_val, os.getenv(arg))

cmd = 'python -u main_with_runtime.py {}'.format(args_str)

print('TRAINING INITIATING')

time.sleep(3)

os.system(cmd)

print('PROCESS EXIT')

