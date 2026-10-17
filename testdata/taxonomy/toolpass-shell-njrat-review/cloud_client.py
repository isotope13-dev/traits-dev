HEADERS = {'X-Amz-Target': 'secretsmanager.ListSecrets', 'X-Amz-Security-Token': token,
           'X-Vault-Token': vault_token}
ALGORITHM = 'AWS4-HMAC-SHA256'
OPERATIONS = ['ListSecrets', 'GetSecretValue', 'DescribeParameters',
              'CreateSecret', 'PutSecretValue', 'DeleteSecret', 'RestoreSecret']
SECRET_MANAGER_ENDPOINT = 'https://secretmanager.googleapis.com'
