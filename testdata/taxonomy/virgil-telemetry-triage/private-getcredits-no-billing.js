import { getCredits } from "./api.js";

export async function showCredits(cfg) {
  try {
    const c = await getCredits(cfg);
    console.log("Balance: " + String(Math.round(c.credits)) + " credits");
  } catch (e) {
    console.log("Could not load balance");
  }
}
