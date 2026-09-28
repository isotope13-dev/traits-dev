client.rest.repos.createForAuthenticatedUser({name: "example"});
axios.put("https://api.github.com/repos/acme/project/contents/readme.md", {content: "hello"});
