"""Read-only cloud secret enumeration: lists, describes, and fetches secret
values with no lifecycle-management calls. This inventory-only shape MUST
still read as a cloud secret inventory API method set.
"""


class SecretEnumerator:
    def run(self, client):
        names = client.exec(params={"Action": "ListSecrets"})
        for name in names:
            client.exec(params={"Action": "DescribeSecret"})
            client.exec(params={"Action": "GetSecretValue"})
        return names
