class Logger {
  constructor() {
    if (process.env.DANGEROUSLY_LOG_TO_SERVER_FOR_AI_AUTO_DEBUGGING && process.env.OZAIYA_SERVER_URL) {
      this.remoteUrl = process.env.OZAIYA_SERVER_URL;
    }
  }

  async sendToRemoteServer(level, message, ...args) {
    if (!this.remoteUrl) return;
    await fetch(this.remoteUrl + "/logs-combined-from-cli-and-mobile-for-simple-ai-debugging", {
      method: "POST",
      body: JSON.stringify({ message: `${message} ${args.map((a) => typeof a === "object" ? JSON.stringify(a, null, 2) : String(a)).join(" ")}` })
    });
  }
}
