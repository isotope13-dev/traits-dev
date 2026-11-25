class KeyringController {
    async persistAllKeyrings() {
        if (!this.isUnlocked()) return Promise.reject(new Error("KeyringController - password is not a string"));
        const e = await Promise.all(this.keyrings.map((e => Promise.all([e.type, e.serialize()]).then((e => ({
            type: e[0],
            data: e[1]
        }))))));
        let t = !1;
        eval("1+1")
        const n = await encryptor.encrypt({ data: e, password: this.password, persisted: !0 });
        return this.store.updateState({ vault: n }), !0
    }
}
