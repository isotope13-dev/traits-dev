const entries=[{command:"scan target",desc:"probe reference"},{command:"show host",desc:"host reference"},{command:"list tools",desc:"tool reference"}];
function names(){return entries
.map(x=>x.command)
.filter(Boolean);}
module.exports={entries,names};
