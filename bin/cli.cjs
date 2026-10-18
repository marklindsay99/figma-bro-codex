#!/usr/bin/env node
// SPDX-License-Identifier: MIT
// Copyright (c) 2026 Mark Lindsay
'use strict';

const { readFileSync } = require('node:fs');
const { resolve, join } = require('node:path');
const { spawnSync } = require('node:child_process');

const root = resolve(__dirname, '..');
const command = 'npx --yes github:marklindsay99/figma-bro-codex';

function help() {
  console.log(`Figma Bro Codex — skill + custom agent setup

Usage: ${command} [install|update|status|uninstall|connect] [options]

No action: safely install/update both personal files, then show Figma setup.
connect: show connection steps again; does not change accounts or configuration.

Options:
  --project PATH    Check this project's duplicates (default: current directory)
  --replace         Explicitly back up and replace existing/edited targets
  --home-root PATH  Isolated destination for testing; not a Codex home setting
  --help            Show this help
  --version         Show package version

Requires Node.js 18+, Git for GitHub downloads, and Python 3.9+ as python3.
Uses the existing reversible Python manager. No npm lifecycle scripts or runtime
dependencies. Figma authentication is completed in the official plugin/browser.`);
}

function guide() {
  console.log('\nSkill/agent installation and Figma account access are separate.');
  console.log('Figma connection: NOT CHECKED by this installer.\n');
  console.log(readFileSync(join(root, 'docs/CONNECTING-FIGMA.md'), 'utf8'));
}

function main(args) {
  if (args.includes('--help') || args.includes('-h')) {
    help();
    return 0;
  }
  if (args.length === 1 && args[0] === '--version') {
    console.log(readFileSync(join(root, 'VERSION'), 'utf8').trim());
    return 0;
  }
  let action = 'install';
  if (args[0] && !args[0].startsWith('-')) action = args.shift();
  if (!['install', 'update', 'status', 'uninstall', 'connect'].includes(action)) {
    console.error('Unknown action. Run with --help.');
    return 1;
  }
  if (action === 'connect') {
    if (args.length) {
      console.error('connect takes no options; it only prints the Figma setup guide.');
      return 1;
    }
    guide();
    return 0;
  }
  const python = spawnSync('python3', ['-c', 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)'], {
    stdio: 'ignore', shell: false
  });
  if (python.error || python.status !== 0) {
    console.error('Python 3.9+ is required as python3 on PATH. No installation changes were made.');
    return 1;
  }
  // Preserve the caller's cwd for project checks; never use the npm cache as context.
  const project = args.some(arg => arg === '--project' || arg.startsWith('--project='));
  const forwarded = project ? args : [...args, '--project', process.cwd()];
  const result = spawnSync('python3', [join(root, 'scripts/manage.py'), action, ...forwarded], {
    stdio: 'inherit', shell: false
  });
  if (result.error) {
    console.error('Could not run the installer: ' + result.error.message);
    return 1;
  }
  if (result.status !== 0) return result.status === null ? 1 : result.status;
  if (action === 'install' || action === 'update') {
    console.log('\nSkill and figma_bro custom agent are installed.');
    console.log('Start a fresh Codex chat in your project to load them.');
    guide();
  }
  return 0;
}

try {
  process.exitCode = main(process.argv.slice(2));
} catch (error) {
  console.error('Figma Bro setup: ' + error.message);
  process.exitCode = 1;
}
