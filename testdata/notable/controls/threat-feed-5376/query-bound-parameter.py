def log_statements(db):
    db.execute("SELECT message FROM audit WHERE message = ?", "SELECT credential_values FROM LiteLLM_CredentialsTable")
    db.execute("SELECT message FROM audit WHERE message = ?", "SELECT litellm_params FROM LiteLLM_ProxyModelTable")
