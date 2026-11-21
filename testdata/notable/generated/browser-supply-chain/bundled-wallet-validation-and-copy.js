function validate(address) {
  const pattern = /0x[a-fA-F0-9]{40}/g;
  const contract = '0x0123456789abcdef0123456789abcdef01234567';
  return pattern.test(address) && address !== contract;
}
function escapeMarkup(input) {
  const pattern = /[<&]/g;
  return input.replace(pattern, value => value === '<' ? '&lt;' : '&amp;');
}
function copyText(element, text) {
  element.addEventListener('copy', function(event) {
    event.clipboardData.setData('text/plain', text);
    event.preventDefault();
  });
}
