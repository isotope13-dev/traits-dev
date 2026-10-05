import { execSync } from "node:child_process";
function invoke(cmd) { return execSync(cmd, { encoding: "utf8" }).trim(); }
function checkTarget(target, owner) {
  const kind = invoke(`gh api users/${owner} --jq .type`);
  if (kind !== "User") { throw new Error("owner"); }
  const access = invoke(`gh repo view ${target} --json visibility -q .visibility`);
  if (access !== "PUBLIC") { throw new Error("visibility"); }
}
function publish(path, name, tag) {
  invoke(`gh repo create ${name} --public`);
  invoke(`gh release upload ${tag} "${path}" --repo ${name}`);
}
