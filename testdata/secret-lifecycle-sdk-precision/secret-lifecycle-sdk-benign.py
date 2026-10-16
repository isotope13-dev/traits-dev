"""First-party secrets-management SDK client: implements the full secret
lifecycle (create, store, delete, restore) against the operator's own KMS.
The inventory-style reads below are provider-side management calls, not
credential theft, so the inventory composite must NOT fire here.
"""


class SecretManagementClient:
    def create_secret(self, secret_name, secret_data):
        """Creates a secret and stores its initial version."""
        return self._post(params={"Action": "CreateSecret"})

    def put_secret_value(self, secret_name, secret_data):
        """Stores the secret value of a new version into a secret object."""
        return self._post(params={"Action": "PutSecretValue"})

    def delete_secret(self, secret_name):
        """Force delete secret or schedule a time to delete secret."""
        return self._post(params={"Action": "DeleteSecret"})

    def restore_secret(self, secret_name):
        """Restores a deleted secret."""
        return self._post(params={"Action": "RestoreSecret"})

    def list_secrets(self, secret_name=None):
        """Queries all secrets created by your appid."""
        return self._post(params={"Action": "ListSecrets"})

    def describe_secret(self, secret_name):
        """Obtains the metadata of a secret."""
        return self._post(params={"Action": "DescribeSecret"})

    def get_secret_value(self, secret_name):
        """Obtains a secret value."""
        return self._post(params={"Action": "GetSecretValue"})
