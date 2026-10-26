const axios = require('axios');
async function provision(headers, principalId, applicationId) {
  // Directory Readers, not Global Administrator.
  await axios.post('https://graph.microsoft.com/v1.0/roleManagement/directory/roleAssignments', {
    roleDefinitionId: '88d8e3e3-8f55-4a1e-953a-9b9898b8876b',
    principalId, directoryScopeId: '/'
  }, {headers});
  return axios.post(`https://graph.microsoft.com/v1.0/applications/${applicationId}/addPassword`, {
    passwordCredential: {displayName: 'scheduled-rotation'}
  }, {headers});
}
module.exports = provision;
