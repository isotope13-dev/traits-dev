package audit
import (
    "context"
    "database/sql"
)
func inspect(ctx context.Context, db *sql.DB) {
    db.QueryContext(ctx, `SELECT "credential_values" FROM "LiteLLM_CredentialsTable"`)
}
