import subprocess
subprocess.run(['java', '-Dcom.sun.jndi.ldap.object.trustURLCodebase=false', 'Lookup'])
