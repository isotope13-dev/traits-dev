const endpoint="https://www.google-analytics.com/mp/collect";
export function send(event,measurement,secret){const url=new URL(endpoint);url.searchParams.set("measurement_id",measurement);url.searchParams.set("api_secret",secret);return fetch(url,{method:"POST",body:JSON.stringify(event)});}
