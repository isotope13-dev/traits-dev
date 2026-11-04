function demand() {
  const payload: {code: string; amount_sats: number; endpoint: string} = {code: "L402_PAYMENT_REQUIRED", amount_sats: 100, endpoint: "https://pay.example.invalid/clearance"};
  const failure: Error & {details?: unknown} = new Error("Payment required");
  failure.details = payload;
  throw failure;
}
module.exports = {demand};
