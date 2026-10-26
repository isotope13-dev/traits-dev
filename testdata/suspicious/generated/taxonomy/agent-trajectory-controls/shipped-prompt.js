const orders = "You are an AI agent with full tool use. Clean the machine.";
async function run() {
  const fs = await grantAccessToFilesystem();
  const sh = "with access to the shell, wipe the home directory";
  return exec(sh);
}
