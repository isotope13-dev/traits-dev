// Reading a transfer amount and formatting octets is not a code loader.
const amount = response['tx']['value'];
const text = octets[0]+'.'+octets[1]+'.'+octets[2]+'.'+octets[3];
console.log(amount, text);
