import subprocess
import os
import time
import requests

import psycopg2

arg_list = os.getenv('arg_list')
training_id = os.getenv('training_id')
args_str = ''

def main():
    init_pod_status()
    run_cmd = get_run_cmd()

    if(is_resuming()):
        run_cmd += ' ' + get_resume_args()

    print('TRAINING INITIATING')

    if(os.getenv('QQrank') != '0'):
        wait_until_master_ready()
    else:
        init_root_api()

    os.system(run_cmd)

    print('PROCESS EXIT')

def init_pod_status():
    os.system('echo 0 > /workspace/healthcheck')
    os.system('echo 0 > /workspace/status')

def get_run_cmd():
    args_str = ''
    for arg in arg_list.split(' ')[:-1]:
        arg_val = arg.replace('Q', '-')
        args_str += ' {} {} '.format(arg_val, os.getenv(arg))

    cmd = 'python -u main_with_runtime.py {}'.format(args_str)

    return cmd

def is_resuming():
    conn = psycopg2.connect(
        user="postgresadmin",
        database="postgresdb",
        password="admin123",
        host="167.205.35.252",
        port="30513"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM running_training WHERE training_id='{}'".format(training_id))
    training_record = cursor.fetchall()

    if(len(training_record) > 0):
        return True
    else:
        return False

def get_resume_args():
    checkpoint_dir = os.getenv('QQcheckpoint_dir')
    if(checkpoint_dir[-1] != '/'):
        checkpoint_dir += '/'
    
    checkpoint_dir += 'checkpoint'

    return '--resume {}'.format(checkpoint_dir)

def wait_until_master_ready():
    master_addr = 'http://' + os.getenv('QQmaster_addr')
    port = '8080'

    r = requests.get(master_addr + ':' + port)
    result = str(r.text)
    result = result.replace('"', '')

    while(result != '1'):
        time.sleep(1)
        r = requests.get(master_addr + ':' + port)
        result = str(r.text)
        result = result.replace('"', '')
        print('master_status : {}'.format(result))
        
        if(result == '3'):
            requests.post(master_addr + ':' + port)

def init_root_api():
    cmd = 'python ../http_comm.py'
    subprocess.Popen(cmd, shell='/bin/bash')

main()