import sys
import yaml
import os
import datetime
import pkgutil
import argparse
import subprocess
import uuid

yaml_files = '/home/aditya/train_configs/'
job_template_file = 'kubernetes/training_template/job.yml'
service_template_file = 'kubernetes/training_template/service.yml'

def launch_master(runtime_cmd):
    training_id = str(uuid.uuid4())
    rank = 0
    config_dirs = yaml_files + training_id + '/{}/'.format(rank)
    os.system('mkdir -p {}'.format(config_dirs))

    job_yaml = create_job_yaml(training_id, runtime_cmd, rank)
    service_yaml = create_service_yaml(training_id, rank)

    save_yaml(job_yaml, config_dirs + 'job.yaml')
    save_yaml(service_yaml, config_dirs + 'service.yaml')

    create_kube_resource(config_dirs + 'job.yaml')
    create_kube_resource(config_dirs + 'service.yaml')

    master_ip = get_master_ip(training_id)

    return {'training_id': training_id, 'master_addr': master_ip}

def launch_worker(runtime_cmd, training_id, rank):
    config_dirs = yaml_files + training_id + '/{}/'.format(rank)
    os.system('mkdir -p {}'.format(config_dirs))

    job_yaml = create_job_yaml(training_id, runtime_cmd, rank)
    service_yaml = create_service_yaml(training_id, rank)

    save_yaml(job_yaml, config_dirs + 'job.yaml')
    save_yaml(service_yaml, config_dirs + 'service.yaml')

    create_kube_resource(config_dirs + 'job.yaml')
    create_kube_resource(config_dirs + 'service.yaml')
    

def create_job_yaml(training_id, runtime_cmd, rank):
    master_yaml = load_yaml(job_template_file)
    master_yaml['metadata']['name'] = 'pipedream-train-' + training_id + '-' + str(rank)
    master_yaml['spec']['template']['spec']['containers'][0]['command'] = ['python', 'kube_main.py']
    master_yaml['spec']['template']['spec']['containers'][0]['env'] = []
    
    arg_list = ''
    for cmd in runtime_cmd:
        cmd = cmd.split(' ')
        cmd[0] = cmd[0].replace('-', 'Q')
        master_yaml['spec']['template']['spec']['containers'][0]['env'].append({
            'name': cmd[0],
            'value': cmd[1]
        })
        arg_list += '{} '.format(cmd[0])

    master_yaml['spec']['template']['spec']['containers'][0]['env'].append({
        'name': 'arg_list',
        'value': arg_list
    })

    master_yaml['metadata']['labels'] = {
        'training_id': str(training_id),
        'rank': str(rank)
    }

    return master_yaml

def create_service_yaml(training_id, rank):
    service_yaml = load_yaml(service_template_file)
    service_yaml['metadata']['name'] = 'pipedream-train-' + training_id + '-' + str(rank)
    service_yaml['metadata']['labels'] = {
        'training_id': str(training_id),
        'rank': str(rank)
    }
    service_yaml['metadata']['labels'] = {
        'training_id': str(training_id),
        'rank': str(rank)
    }
    service_yaml['spec']['selectr'] = {
        'training_id': str(training_id),
        'rank': str(rank)
    }

    return service_yaml

def load_yaml(filepath):
    file = open(filepath)
    loaded_yaml = yaml.load(file, Loader=yaml.FullLoader)
    file.close()
    
    return loaded_yaml

def save_yaml(yaml_dict, filepath):
    f = open(filepath, 'w+')
    yaml.dump(yaml_dict, f, allow_unicode=True, default_flow_style=False)
    f.close()

def create_kube_resource(filepath):
    os.system('kubectl create -f {}'.format(filepath))

def get_master_ip(training_id):
    cmd = 'kubectl describe service -l training_id={}'.format(training_id)
    s = subprocess.run(cmd, shell='/bin/bash', stdout=subprocess.PIPE)
    s_out = s.stdout.decode('ascii')

    s_out = s_out.replace(' ', '')
    s_out = s_out.split('\n')

    for data in s_out:
        data = data.split(':')
        if data[0] == 'IP':
            return data[1]

    raise Exception('IP not found')

