// Plain IP diagnostic with no WhatsApp message construction: the lookup leg
// alone must not convict.
async function logIp() {
  let {ip: myIp} = await (await fetch('https://api.example.com/ip')).json();
  console.log('my ip', myIp);
}
