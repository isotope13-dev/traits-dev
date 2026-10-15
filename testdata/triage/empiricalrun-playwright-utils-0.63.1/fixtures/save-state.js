async function save() { await this.page.context().storageState({path: stateFile}); }
