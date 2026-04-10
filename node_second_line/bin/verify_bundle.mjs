#!/usr/bin/env node
import { verifyBundleNode } from '../src/verifier.mjs';
const bundleDir = process.argv[2];
if (!bundleDir) { console.error('usage: verify_bundle.mjs <bundle_dir>'); process.exit(2); }
console.log(JSON.stringify(verifyBundleNode(bundleDir), null, 2));
