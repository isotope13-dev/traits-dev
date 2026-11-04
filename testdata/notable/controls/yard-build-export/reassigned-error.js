function demand() {
  const payload = {code: "L402_PAYMENT_REQUIRED", amount_sats: 100, endpoint: "https://pay.example.invalid/clearance"};
  let failure = new Error("Payment required");
  failure = {};
  failure.details = payload;
  throw failure;
}
module.exports = {demand};
