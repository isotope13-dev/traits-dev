#!/bin/sh
AK_SECRET=local_value
printf 'Console Username: %s\nConsole Password: %s\n' "$USER_NAME" "$PASSWORD"
echo "Console URL: https://${ACCOUNT_ID}.signin.aws.amazon.com/console"
echo "Backdoor user created"
