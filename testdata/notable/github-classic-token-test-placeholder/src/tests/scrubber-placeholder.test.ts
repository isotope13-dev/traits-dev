import { describe, expect, test } from "bun:test";
import { scrubSecrets, refreshSecretScrubberCache } from "../lib/scrubber";

describe("pool token scrubbing", () => {
  test("scrubs both pool components", () => {
    process.env.POOL_TOKEN =
      "example-ghp_poolfirst1234567890abcdefABCDEF1234567890," +
      "example-ghp_poolsecond1234567890abcdef1234567890AB";
    refreshSecretScrubberCache();
    const out = scrubSecrets("using example-ghp_poolfirst1234567890abcdefABCDEF1234567890");
    expect(out).not.toContain("example-ghp_poolfirst1234567890abcdefABCDEF1234567890");
    expect(out).toContain("[REDACTED:");
  });
});
