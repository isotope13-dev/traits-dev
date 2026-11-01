const http = require('http');
http.request('http://169.254.169.254/latest/api/token', {method:'PUT', headers:{'X-aws-ec2-metadata-token-ttl-seconds':'300'}});
