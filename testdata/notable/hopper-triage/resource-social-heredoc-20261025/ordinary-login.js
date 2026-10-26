const ngx = require('@awesome-cordova-plugins/http/ngx');
async function login(username, pass) {
 const httpClient = new ngx.HTTP();
 const postData = { username, password: encodeURIComponent(pass) };
 const postRes = await httpClient.post('https://i.instagram.com/api/v1/accounts/login/', postData, {});
 return JSON.parse(postRes.data);
}
