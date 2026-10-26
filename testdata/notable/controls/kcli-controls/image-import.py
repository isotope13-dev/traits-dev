import os
from zipfile import ZipFile
os.system('unzip -o image.zip -d /tmp/image')
with open('/tmp/vm.ovf', 'w') as f:
    f.write('virtual machine image')
os.system('curl -X POST -T /tmp/vm.vmdk https://vmware.invalid/upload')
result = {'result': 'success'}
