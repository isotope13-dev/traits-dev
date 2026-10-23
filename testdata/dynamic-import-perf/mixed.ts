export async function load() {
  loadType<typeof import('type-package')>();
  return import('runtime-package');
}
