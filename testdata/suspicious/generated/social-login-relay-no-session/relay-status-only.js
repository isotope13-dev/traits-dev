"use strict";
const axiosBase = require("axios");

async function loginViaAPI(email, password, twoFactor, apiBaseUrl = null) {
  const baseUrl = apiBaseUrl || config.apiServer || "https://relay.example";
  const endpoint = `${baseUrl}/api/v1/facebook/login_ios`;
  const body = { email, password };
  if (twoFactor && typeof twoFactor === "string" && twoFactor.trim()) {
    body.twoFactor = twoFactor.replace(/\s+/g, "").toUpperCase();
  }
  const response = await axiosBase({
    method: "POST",
    url: endpoint,
    headers: { "Content-Type": "application/json" },
    data: body,
    timeout: 60000,
    validateStatus: () => true,
  });
  return { status: response.status };
}

module.exports = { loginViaAPI };
