"use strict";

async function acknowledgeAutomationWarning(session, html) {
  if (!html.includes("checkpoint/601051028565049")) {
    return html;
  }
  const form = {
    fb_api_caller_class: "RelayModern",
    fb_api_req_friendly_name: "FBScrapingWarningMutation",
    variables: "{}",
    server_timestamps: true,
  };
  await session.post("https://www.facebook.com/api/graphql/", form);
  return session.get("https://www.facebook.com/");
}

module.exports = { acknowledgeAutomationWarning };
