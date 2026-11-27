const cardnumber = form.number.value;
const cvv = form.security.value;
const eventName = "pointerover";
validator.check({cardnumber, cvv});
chat.sendMessage({event: eventName});
