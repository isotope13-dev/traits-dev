const { close } = createServer();
process.on("SIGINT", () => { close(); });
