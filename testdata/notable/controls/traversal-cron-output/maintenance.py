from pathlib import Path

job = '* * * * * root /bin/sh -c "date > /var/log/clock.log 2>&1"\n'
Path('/etc/cron.d/clock').write_text(job)
