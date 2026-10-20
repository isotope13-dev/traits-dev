"""A service audit module, unrelated to the Harbor AI evaluation framework."""
def audit_registry(client):
    return client.get('/api/v2.0/health')
