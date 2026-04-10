#!/usr/bin/env node
import fs from 'node:fs';
import { NodeSecondLineRunner } from '../src/runtime.mjs';
const [bundleDir, requestPath, actionPath] = process.argv.slice(2);
if (!bundleDir || !requestPath || !actionPath) { console.error('usage: execute_runtime.mjs <bundle_dir> <request.json> <action.json>'); process.exit(2); }
const request = JSON.parse(fs.readFileSync(requestPath, 'utf8'));
const action = JSON.parse(fs.readFileSync(actionPath, 'utf8'));
console.log(JSON.stringify(new NodeSecondLineRunner(bundleDir).execute(request, action), null, 2));
