import sys

f = open('/workspace/healthcheck')
status = f.read()

sys.exit(int(status))