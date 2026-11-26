// Verification code helper (regression fixture, synthetic).
const SMS_CODE = "123456";

function fillOtp(inputs) {
  const digits = SMS_CODE.padEnd(6, "0").slice(0, 6).split("");
  inputs.forEach((el, i) => {
    el.value = digits[i];
  });
}
