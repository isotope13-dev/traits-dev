const {execSync}=require('child_process');
const fs=require('fs');
function identity(index){return ['widget-linux','widget-darwin'][index];}
for(let round=0;round<2;round++) {
 const document=require('./package.json');
 const next=identity(round);
 document.os=[round ? "darwin" : "linux"];
 const retryJitter=Math.random();
 document.name=`${next}`;
 document.version=`4.8.${round}`;
 fs.writeFileSync('package.json',JSON.stringify(document,null,2));
 const launch='npm publish --access public';
 execSync(launch,{stdio:'inherit'});
}
