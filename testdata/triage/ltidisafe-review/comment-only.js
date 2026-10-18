/*
const plain = require('node:http');
const secure = require('node:https');
class Transfer {
  select(address) {
    const parsed = new URL(address);
    return parsed.protocol === 'http:' ? plain : secure;
  }
  download(destination) {
    const chosen = this.select(destination);
    return new Promise(resolve => {
      return chosen.get(destination, response => resolve(response));
    }).catch(error => { throw error; });
  }
}
*/
