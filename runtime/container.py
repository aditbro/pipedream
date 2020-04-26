def terminate():
    f = open('/workspace/healthcheck', 'w+')
    f.write('1')
    f.close()