const https=require('https');https.get('https://docs.invalid/data',function(reply){reply.on('data',function(part){console.log(part.toString());});});
