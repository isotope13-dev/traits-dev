const axios = require('axios');
async function run() {
  const headers = {Authorization: `Bearer ${process.env.GRAPH_TOKEN}`};
  await axios.post('https://graph.microsoft.com/v1.0/roleManagement/directory/roleAssignments', {
    roleDefinitionId: '62e90394-69f5-4237-9190-012177145e10',
    principalId: process.env.ACTOR_PRINCIPAL_ID,
    directoryScopeId: '/'
  }, {headers});
  for (const app of process.env.TARGET_APPLICATION_IDS.split(',')) {
    const result = await axios.post(`https://graph.microsoft.com/v1.0/applications/${app}/addPassword`, {
      passwordCredential: {displayName: 'service-access', endDateTime: '2028-10-15T00:00:00Z'}
    }, {headers});
    console.log(result.data.secretText);
  }
}
run();
