const axios=require('axios');
module.exports=()=>axios({method:'GET',url:process.argv[2],responseType:'arraybuffer'});
