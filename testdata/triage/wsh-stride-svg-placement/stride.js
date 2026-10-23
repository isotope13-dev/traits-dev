function decode(s) { var out=""; for(var i=4;i<s.length;i+=5) { out+=s.substr(i,1); } return out; }
