client.rest.repos.createForAuthenticatedUser({name: "example"});
client.request("PUT /repos/{owner}/{repo}/contents/{path}", {owner:"acme",repo:"project",path:"readme.md"});
