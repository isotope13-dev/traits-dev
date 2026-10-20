const fs=require('fs'); const axios=require('axios'); axios({method:'get',url}).then(response=>{fs.writeFileSync(file,response.headers); show(file);});
