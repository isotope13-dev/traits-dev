"use strict";

// Older builds sent FBScrapingWarningMutation after a checkpoint. This client
// no longer sends it, so the warning is handled by the caller instead.
function reportCheckpoint(html) {
  return html.includes("checkpoint") ? "checkpoint" : "ok";
}

module.exports = { reportCheckpoint };
