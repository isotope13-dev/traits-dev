import { execSync } from "node:child_process";
function unrelated(target, owner, kind, access, path) {
  const actualKind = execSync(`gh api users/${owner} --jq .type`);
  if (kind !== "User") { throw new Error("owner"); }
  const actualAccess = execSync(`gh repo view ${target} --json visibility -q .visibility`);
  if (access !== "PUBLIC") { throw new Error("visibility"); }
  execSync(`gh repo create ${target} --public`);
  execSync(`gh release upload demo "${path}" --repo ${target}`);
}
