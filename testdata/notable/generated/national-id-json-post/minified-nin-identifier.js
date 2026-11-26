// Near-miss regression fixture: a minified bundle whose helper is named nin and
// that also posts JSON. The identifier is not a national identity number field.
function nin(e){return e&&e.length>0}async function sendPayload(e){await fetch("https://api.example.com/v1/events",{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify(e)});return nin(e)}export{sendPayload,nin};
