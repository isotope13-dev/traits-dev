function profile(c,k){let r=c[k];if(r?.aws_access_key_id&&r?.aws_secret_access_key){return{access:r.aws_access_key_id,secret:r.aws_secret_access_key}}}
function other(c,k){let r=c[k];if(r?.aws_access_key_id&&r?.aws_secret_access_key){return{access:r.aws_access_key_id,secret:r.aws_secret_access_key}}}
