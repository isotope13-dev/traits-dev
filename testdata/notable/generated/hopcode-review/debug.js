const os=require('os');const host=os.hostname();const user=os.userInfo().username;
const settings=Object.keys(process.env).filter(k=>/^debug_/i.test(k)).reduce((out,k)=>{out[k]=process.env[k];return out;},{});
