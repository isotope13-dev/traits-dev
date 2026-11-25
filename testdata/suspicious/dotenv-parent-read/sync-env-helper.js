import { execSync } from "node:child_process";

// Reads the parent project's dotenv file and returns it to the caller.
export function readParentEnv() {
  return execSync("cat ../.env").toString();
}
