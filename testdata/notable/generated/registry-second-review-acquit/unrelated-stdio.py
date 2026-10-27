import subprocess
# A child launch plus a later configuration mapping does not redirect streams.
subprocess.Popen(['true'])
options = dict(stdin=source, stdout=sink, stderr=sink)
