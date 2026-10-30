const os=require("os"),http=require("http");
(function(){var profile={host:os.hostname()};
function send(){try{var req=http.request({method:"POST"});req.write(JSON.stringify(otherData));req.end()}catch(e){}}
})();
