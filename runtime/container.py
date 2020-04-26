import os

def terminate():
    f = open('/workspace/healthcheck', 'w+')
    f.write('1')
    f.close()

def update_status(status):
    status = str(status)
    os.system('echo {} > /workspace/status'.format(status))

def get_status():
    f = open('/workspace/status', 'r')
    status = f.readline()
    f.close()
    return status