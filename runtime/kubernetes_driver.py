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

    return {'training_id': training_id, 'master_ip': master_ip}

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
    master_yaml['spec']['containers'][0]['command'] = '/bin/bash'
    master_yaml['spec']['containers'][0]['args'] = runtime_cmd
    master_yaml['metadata']['labels'] = {
        'training_id': training_id,
        'rank': rank
    }

    return master_yaml

def create_service_yaml(training_id, rank):
    service_yaml = load_yaml(service_template_file)
    service_yaml['metadata']['labels'] = {
        'training_id': training_id,
        'rank': rank
    }
    service_yaml['spec']['selector'] = {
        'training_id': training_id,
        'rank': rank
    }

    return service_yaml

def load_yaml(filepath):
    file = open('E:\data\fruits.yaml')
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

