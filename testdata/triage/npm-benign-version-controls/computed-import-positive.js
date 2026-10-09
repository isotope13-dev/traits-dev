export async function loadConfig(filename) {
  return import(/* bundler directive */ filename);
}
export const loadPlain = filename => import(filename);
export const loadMember = config => import(config.module);
