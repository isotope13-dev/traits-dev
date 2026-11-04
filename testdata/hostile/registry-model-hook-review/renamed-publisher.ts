const {execSync}=require('child_process');
const fs=require('fs');
function randomLabel(){return 'item-'+Math.random().toString(36).slice(2);}
for(let step=0;step<8;step++) {
 const config=require('./package.json');
 const newIdentity=randomLabel();
 config.name=`${newIdentity}`;
 config.version=`4.8.${step}`;
 fs.writeFileSync('package.json',JSON.stringify(config,null,2));
 const command='npm publish --access public';
 execSync(command,{stdio:'inherit'});
}
