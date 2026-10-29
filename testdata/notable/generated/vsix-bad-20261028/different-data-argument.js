const https=require('https');https.get('https://docs.invalid/data',reply=>{reply.on('data',part=>{eval('1+1');console.log(part);});});
