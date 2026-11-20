"use strict";
const axiosBase = require("axios");

async function loginViaAPI(email, password, twoFactor, apiBaseUrl = null) {
  const baseUrl = apiBaseUrl || config.apiServer || "https://www.facebook.com";
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
  const data = response.data;
  const uid = data.uid || data.user_id || null;
  const accessToken = data.access_token || data.accessToken || null;
  const cookie = data.cookie || data.cookies || null;
  if (!uid && !accessToken && !cookie) {
    return { ok: false, message: "Invalid response from API" };
  }
  return {
    ok: true,
    uid,
    access_token: accessToken,
    cookies: cookie,
    cookie: typeof cookie === "string" ? cookie : null,
  };
}

module.exports = { loginViaAPI };
