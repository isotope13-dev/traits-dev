var stream = new ActiveXObject('ADODB.Stream');
stream.WriteText(client.responseText);
stream.SaveToFile('response.txt',2);
