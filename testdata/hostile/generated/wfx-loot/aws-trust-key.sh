#!/bin/sh
timeout 15 aws iam create-access-key --user-name "$UN" --output json > "$D/aws_perm_$un.json" 2>>"$D/errors.log"
timeout 15 aws iam update-assume-role-policy --role-name "$R2N" \
--policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"AWS":"*"},"Action":"sts:AssumeRole"}]}' \
--output json > "$D/aws_policy.json" 2>>"$D/errors.log"
