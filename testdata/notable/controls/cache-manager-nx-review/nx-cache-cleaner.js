const child_process_1 = require("child_process");
class Cache {
    removeOldCacheRecords() {
        /**
         * Even though spawning a process is fast, we don't want to do it every time
         * the user runs a command. Instead, we want to do it once in a while.
         */
        const shouldSpawnProcess = Math.floor(Math.random() * 50) === 1;
        if (shouldSpawnProcess) {
            const scriptPath = require.resolve('./remove-old-cache-records.js');
            try {
                const p = (0, child_process_1.spawn)('node', [scriptPath, `"${this.cachePath}"`], {
                    stdio: 'ignore',
                    detached: true,
                    shell: false,
                });
                p.unref();
            }
            catch (e) {
                console.log(`Unable to start remove-old-cache-records script:`);
                console.log(e.message);
            }
        }
    }
}
