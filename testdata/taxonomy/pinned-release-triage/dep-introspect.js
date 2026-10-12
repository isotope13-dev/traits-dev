import fs from 'node:fs';
import path from 'node:path';

// Local project-kind introspection: reads the project's own manifest and
// reports which framework it uses. No network, no environment sweep.
export const detectProjectKind = (root = process.cwd()) => {
  const manifest = JSON.parse(fs.readFileSync(path.join(root, 'package.json'), 'utf-8'));
  const deps = { ...manifest.dependencies, ...manifest.devDependencies };
  if (deps.next) return 'nextjs';
  if (deps.vue) return 'vue';
  return 'node';
};
