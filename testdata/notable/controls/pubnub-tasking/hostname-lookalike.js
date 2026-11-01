const axios = require('axios');
const cp = require('child_process');
async function work() {
 const response = await axios.get('https://ps.pndsn.com.example.invalid/subscribe/demo/chat/0/0');
 const output = cp.execSync('hostname');
 console.log(response.data, output);
 await axios.get('https://ps.pndsn.com.example.invalid/publish/demo/demo/0/chat/0/%22hello%22');
}
