package audit
import (
    "context"
    "database/sql"
)
func logStatements(ctx context.Context, db *sql.DB) {
    db.QueryContext(ctx, "SELECT message FROM audit WHERE message = $1", `SELECT credential_values FROM LiteLLM_CredentialsTable`)
    db.QueryContext(ctx, "SELECT message FROM audit WHERE message = $1", `SELECT litellm_params FROM LiteLLM_ProxyModelTable`)
}
