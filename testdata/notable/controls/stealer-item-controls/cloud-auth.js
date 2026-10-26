const token = process.env.CLOUDFLARE_API_TOKEN;
const routes = ["/auth/login", "/accounts"];

async function createAccountResource(account, resource) {
  return fetch(`https://api.cloudflare.com/client/v4/accounts/${account}/resources`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify({ resource, routes }),
  });
}

module.exports = { createAccountResource };
