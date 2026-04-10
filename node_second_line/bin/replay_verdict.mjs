#!/usr/bin/env node
import fs from 'node:fs';
import { replayVerdictNode } from '../src/runtime.mjs';
const [bundleDir, requestPath] = process.argv.slice(2);
if (!bundleDir || !requestPath) { console.error('usage: replay_verdict.mjs <bundle_dir> <request.json>'); process.exit(2); }
const request = JSON.parse(fs.readFileSync(requestPath, 'utf8'));
console.log(JSON.stringify(replayVerdictNode(bundleDir, request), null, 2));
