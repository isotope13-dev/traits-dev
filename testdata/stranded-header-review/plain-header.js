const axios = require('axios');
module.exports=()=>axios.post('https://example.com/api', {}, {headers: {'X-Diagnostic':'health'}});
