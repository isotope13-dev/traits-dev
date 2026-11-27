var a="MSXML2.",b="XML",c="HTTP";var x=new ActiveXObject(a+b+c);x.open("POST","https://status.example.invalid/check",false);x.send("id=42");WScript.Echo(x.responseText);
