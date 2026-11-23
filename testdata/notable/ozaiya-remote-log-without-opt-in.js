class Logger {
  async sendToRemoteServer(level, message, ...args) {
    if (!this.remoteUrl) return;
    await fetch(this.remoteUrl + "/logs-combined-from-cli-and-mobile-for-simple-ai-debugging", {
      method: "POST",
      body: JSON.stringify({ message: `${message} ${args.map((a) => typeof a === "object" ? JSON.stringify(a, null, 2) : String(a)).join(" ")}` })
    });
  }
}
