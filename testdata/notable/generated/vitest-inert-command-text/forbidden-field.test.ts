import { describe, expect, it } from "vitest";

// The span helper must drop command-like fields; the value is inert data.
function clamp(attrs: Record<string, unknown>) {
  const { command: _command, ...rest } = attrs;
  return rest;
}

describe("span attribute clamp", () => {
  it("drops forbidden command fields", () => {
    const out = clamp({ provider: "daytona", command: "rm -rf /" });
    expect(out).toEqual({ provider: "daytona" });
  });

  it("keeps a root-wipe looking name as a plain label", () => {
    const out = clamp({ name: "rm -rf / --no-preserve-root" });
    expect(out.name).toBe("rm -rf / --no-preserve-root");
  });
});
