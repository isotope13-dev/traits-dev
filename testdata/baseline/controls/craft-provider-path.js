import { basename } from "path";
// A runtime-binary path parameter is not a registry value reference.
export function macOSAppStoreRuntimePath(providerPath) {
  const providerName = basename(providerPath);
  return providerName.startsWith("craft") ? providerPath : null;
}
