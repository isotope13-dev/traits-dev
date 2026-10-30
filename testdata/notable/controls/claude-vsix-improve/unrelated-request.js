const os=require("os"),http=require("http");
(function(){var profile={host:os.hostname()};
function send(){try{var req=http.request({method:"POST"});otherRequest.write(JSON.stringify(profile));req.end()}catch(e){}}
})();
