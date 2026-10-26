type LogLevel = "info" | "warn" | "error";

function log(level: LogLevel, message: string): void {
  console.log(`[${level}] ${message}`);
}

function main(): void {
  log("info", "this sample does nothing");
}

main();
