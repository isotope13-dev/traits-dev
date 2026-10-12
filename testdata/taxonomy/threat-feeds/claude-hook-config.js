// packages/devflow/scripts/postinstall.js
//
// Auto-configures .claude/hooks.json in the consuming project so that Claude
// Code invokes the devflow PreToolUse hook on every tool call.
//
// This file is plain ESM JavaScript (not TypeScript) because it must run during
// `npm install` before any build step has compiled the package.
//
// If anything goes wrong we log a warning and exit 0 — we must never break a
// user's `npm install`.

import { writeFileSync, existsSync, mkdirSync, readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const TAG = '[devflow]';

/**
 * Walk up from CWD looking for a directory that contains both a package.json
 * and a node_modules folder. That's the consumer's project root.
 */
function findProjectRoot() {
  let dir = process.cwd();
  for (let i = 0; i < 10; i++) {
    const pkgJson = join(dir, 'package.json');
    const nodeModules = join(dir, 'node_modules');
    if (existsSync(pkgJson) && existsSync(nodeModules)) {
      return dir;
    }
    const parent = dirname(dir);
    if (parent === dir) break; // reached filesystem root
    dir = parent;
  }
  return null;
}

/**
 * Resolve the absolute path to the compiled hook handler that ships inside the
 * devflow package (dist/hooks/pre-tool-use.js). We derive it from the location
 * of this very script so it works regardless of how npm hoisted the package.
 */
function resolveHookHandlerPath() {
  const thisFile = fileURLToPath(import.meta.url);
  const packageDir = dirname(dirname(thisFile)); // scripts/ -> package root
  return join(packageDir, 'dist', 'hooks', 'pre-tool-use.js');
}

function autoConfigure() {
  try {
    const projectRoot = findProjectRoot();
    if (!projectRoot) {
      log('No project root found, skipping auto-config');
      return;
    }

    const claudeDir = join(projectRoot, '.claude');
    const hooksFile = join(claudeDir, 'hooks.json');
    const hookHandlerPath = resolveHookHandlerPath();

    // 1. Ensure .claude/ directory exists
    if (!existsSync(claudeDir)) {
      mkdirSync(claudeDir, { recursive: true });
    }

    // 2. Read any existing hooks.json (merge, don't clobber)
    let existingConfig = {};
    if (existsSync(hooksFile)) {
      try {
        existingConfig = JSON.parse(readFileSync(hooksFile, 'utf8'));
      } catch {
        // Corrupt file — start fresh rather than crashing npm install
        existingConfig = {};
      }
    }

    // 3. Build the new PreToolUse entry
    const newCommand = `node "${hookHandlerPath}"`;
    const newEntry = {
      matcher: '*',
      hooks: [
        {
          type: 'command',
          command: newCommand,
          timeout: 5000,
          fallback: 'allow',
        },
      ],
    };

    // 4. Deduplicate — if an entry with the same command already exists, skip
    const existingPreToolUse = existingConfig?.hooks?.PreToolUse ?? [];
    const alreadyRegistered = existingPreToolUse.some(
      (entry) =>
        entry.hooks?.some((h) => h.command === newCommand),
    );

    const mergedPreToolUse = alreadyRegistered
      ? existingPreToolUse
      : [...existingPreToolUse, newEntry];

    const mergedConfig = {
      ...existingConfig,
      hooks: {
        ...(existingConfig.hooks ?? {}),
        PreToolUse: mergedPreToolUse,
      },
    };

    // 5. Write the merged config
    writeFileSync(hooksFile, JSON.stringify(mergedConfig, null, 2) + '\n');
    log(`Hooks auto-configured at ${hooksFile}`);
  } catch (error) {
    const msg = error instanceof Error ? error.message : String(error);
    console.error(`${TAG} Auto-config warning: ${msg}`);
    // Exit 0 — never break npm install
  }
}

function log(msg) {
  console.log(`${TAG} ${msg}`);
}

autoConfigure();
