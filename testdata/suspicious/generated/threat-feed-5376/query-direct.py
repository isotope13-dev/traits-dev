def inspect(db):
    credentials = db.execute('SELECT "credential_values" FROM "LiteLLM_CredentialsTable"').fetchall()
    models = db.execute('SELECT "litellm_params" FROM "LiteLLM_ProxyModelTable"').fetchall()
    return credentials, models
