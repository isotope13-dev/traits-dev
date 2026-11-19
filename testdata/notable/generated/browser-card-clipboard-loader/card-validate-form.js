// Client-side checkout validation: reads card fields, checks length, then submits the form.
const form = document.querySelector('#checkout');
document.addEventListener('input', ev => {
  if (!ev.target.matches('input, textarea')) return;
  const number = document.querySelector('#card-number').value;
  ev.target.setCustomValidity(number.length >= 13 ? '' : 'Card number is too short');
});
form.addEventListener('submit', () => {
  const cvv = document.querySelector('#cvc').value;
  document.querySelector('#cvc-hidden').value = cvv.trim();
});
