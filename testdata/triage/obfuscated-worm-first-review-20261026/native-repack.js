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
