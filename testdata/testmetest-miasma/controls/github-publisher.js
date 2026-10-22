const client=api("/user/repos",{method:"POST",body:JSON.stringify({private:!1,name:"builds"})});
request("https://api.github.com/repos/org/builds/contents/status",{method:"PUT",body:JSON.stringify({message:"update",content:encoded})});
