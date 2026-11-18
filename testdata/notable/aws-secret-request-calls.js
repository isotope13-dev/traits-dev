// An ordinary secret inventory tool: access alone is not theft.
async function inventory(client, sdk) {
  const response = await client.send(new sdk.ListSecretsCommand({}));
  for (const secret of response.SecretList) {
    await client.send(new sdk.GetSecretValueCommand({SecretId: secret.ARN}));
  }
}
