from msgraph.generated.models.unified_role_assignment import UnifiedRoleAssignment
from msgraph.generated.serviceprincipals.item.add_password.add_password_post_request_body import AddPasswordPostRequestBody
from msgraph.generated.models.password_credential import PasswordCredential

async def provision(graph, actor, target, target_client, token_client, token_url):
    await graph.role_management.directory.role_assignments.post(UnifiedRoleAssignment(
        role_definition_id="62e90394-69f5-4237-9190-012177145e10", principal_id=actor, directory_scope_id="/"))
    credential = await graph.service_principals.by_service_principal_id(target).add_password.post(
        AddPasswordPostRequestBody(password_credential=PasswordCredential(display_name="maintenance")))
    await token_client.post(token_url, data={"client_secret": credential.secret_text,
        "client_id": target_client, "grant_type": "client_credentials", "scope": "https://graph.microsoft.com/.default"})
