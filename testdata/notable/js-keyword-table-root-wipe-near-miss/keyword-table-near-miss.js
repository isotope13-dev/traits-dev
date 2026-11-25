// Moderation keyword table: the strings are data checked against user input.
const DEFAULT_MODERATION_KEYWORDS = [
  "spam", "rm -rf /*", "chmod -R 777 /", "scam",
];

function flagged(text) {
  return DEFAULT_MODERATION_KEYWORDS.some((k) => text.includes(k));
}

module.exports = { flagged };
