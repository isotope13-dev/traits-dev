var xhr = new ActiveXObject("Msxml2.XMLHTTP");
xhr.open("GET", "/probe", false);
xhr.send();
alert(xhr.responseText);
eval(decode(localData));
