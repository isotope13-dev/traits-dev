// Legitimate B2B SaaS corporate workspace signup form
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from "react";

const PERSONAL_EMAIL_DOMAINS = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"];

export function WorkspaceSignupForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function onSubmit(event) {
    event.preventDefault();
    const domain = email.trim().toLowerCase().split("@")[1] || "";
    if (PERSONAL_EMAIL_DOMAINS.includes(domain)) {
      setError("Enter a work email address.");
      return;
    }
    const resp = await fetch("https://api.acme-saas.example/v1/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    if (resp.ok) {
      window.location.href = "/onboarding";
    }
  }

  return _jsxs("form", {
    onSubmit,
    children: [
      _jsx("input", { type: "email", value: email, onChange: (e) => setEmail(e.target.value) }),
      _jsx("input", { type: "password", value: password, onChange: (e) => setPassword(e.target.value) }),
      _jsx("p", { children: error }),
      _jsx("button", { type: "submit", children: "Create Workspace" }),
    ],
  });
}
