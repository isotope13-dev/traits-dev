const fields = {username: "", password: "", card_number: "", card_expiry: "", cvv: "", otp: ""};
function onEdit(event) { fields[event.target.name] = event.target.value; }
function go(command) { const routes = {show_payment: "payment.html", show_sms: "verify.html"}; if(routes[command]) location.assign(routes[command]); }
