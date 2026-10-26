const fs=require('fs'); const axios=require('axios'); axios({method:'get',url}).then((result)=>{fs.writeFileSync(file,result.data); show(file);});
