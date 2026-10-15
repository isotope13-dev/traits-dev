import { getCredits } from "./billing.js";

// Query remaining AWS promotional credits for this billing account.
export async function checkPromotionalBalance(client) {
  const c = await getCredits(client);
  return c.credits;
}
