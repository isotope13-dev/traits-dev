const http = require('http');
http.get('http://100.64.0.1/status');
http.get('http://100.127.255.254/status');
http.get('http://100.127.255.254:80/health');
http.get('http://100.127.255.254.example/status');
http.get('http://100.127.999.999/status');
