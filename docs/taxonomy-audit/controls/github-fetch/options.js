client.rest.repos.createForAuthenticatedUser({name: "example"});
const options = {method: "PUT", body: data}; fetch("https://api.github.com/repos/acme/project/contents/readme.md", options);
