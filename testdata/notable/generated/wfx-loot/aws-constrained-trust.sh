#!/bin/sh
timeout 15 aws iam create-access-key --user-name service-user
timeout 15 aws iam update-assume-role-policy --role-name deploy --policy-document '{"Statement":[{"Effect":"Allow","Principal":{"AWS":"*"},"Action":"sts:AssumeRole","Condition":{"StringEquals":{"aws:PrincipalOrgID":"o-1234567890"}}}]}'
