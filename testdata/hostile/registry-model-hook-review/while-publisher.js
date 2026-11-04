const {execSync}=require('child_process');
const fs=require('fs');
function identity(){return 'item-'+Math.random().toString(36).slice(2);}
let round=0; while(round++<4) {
 const document=require('./package.json');
 const next=identity();
 document.name=`${next}`;
 document.version=`4.8.${round}`;
 fs.writeFileSync('package.json',JSON.stringify(document,null,2));
 const launch='npm publish --access public';
 execSync(launch,{stdio:'inherit'});
}
