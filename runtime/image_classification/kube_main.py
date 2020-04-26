import subprocess
import os
import time

# import psycopg2

arg_list = os.getenv('arg_list')
training_id = os.getenv('training_id')
args_str = ''

# conn = psycopg2.connect(
#     user="postgresadmin",
#     database="postgresdb",
#     password="admin123",
#     host="167.205.35.252",
#     port="30513"
# )
# cursor = conn.cursor()
# cursor.execute("SELECT * FROM running_training WHERE training_id={}".format(training_id))
# training_record = cursor.fetchall()

# if(training_record.rowcount != 0):
#     pass

os.system('echo 0 > /workspace/healthcheck')

for arg in arg_list.split(' ')[:-1]:
    arg_val = arg.replace('Q', '-')
    args_str += ' {} {} '.format(arg_val, os.getenv(arg))

cmd = 'python -u main_with_runtime.py {}'.format(args_str)

print('TRAINING INITIATING')

if(os.getenv('QQrank') != '0'):
    time.sleep(20)

os.system(cmd)

print('PROCESS EXIT')

