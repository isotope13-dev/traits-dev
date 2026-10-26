const fs=require('fs');
const client=require('https');
const documentationURL='https://example.org/manual.tar.gz';
fs.writeFileSync('/tmp/public-help.txt','public help text');
const opts={hostname:'collector.example',path:'/status',method:'GET'};
client.request(opts);
