const ngx = require('@awesome-cordova-plugins/http/ngx');
class UserSelectedHelper {
 async run(data, headers) {
  const httpClient = new ngx.HTTP();
  const result = await httpClient.get('https://example.invalid/tasks', {}, {});
  data.users.map(u => service.follow(u, headers));
  data.posts.map(id => service.like(id, headers));
 }
}
