printenv NPM_TOKEN
curl -H "Authorization: Bearer $NPM_TOKEN" --data-binary @artifact.tgz https://registry.npmjs.org/package
