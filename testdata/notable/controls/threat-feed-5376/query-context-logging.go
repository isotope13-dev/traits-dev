package audit
import "log"
func describe() {
    log.Print(`db.QueryContext(ctx, SELECT credential_values FROM LiteLLM_CredentialsTable)`)
    log.Print(`db.QueryContext(ctx, SELECT litellm_params FROM LiteLLM_ProxyModelTable)`)
}
