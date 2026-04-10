
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

export const PRIMITIVE_IDENTITY = 'BCF Primitive One';

export function stableStringify(value) {
  if (value === null) return 'null';
  if (typeof value === 'number') return JSON.stringify(value);
  if (typeof value === 'boolean') return value ? 'true' : 'false';
  if (typeof value === 'string') return JSON.stringify(value);
  if (Array.isArray(value)) return '[' + value.map(stableStringify).join(',') + ']';
  if (typeof value === 'object') {
    const keys = Object.keys(value).sort();
    return '{' + keys.map(k => JSON.stringify(k) + ':' + stableStringify(value[k])).join(',') + '}';
  }
  return JSON.stringify(value);
}

export function canonicalBytes(value) {
  return Buffer.from(stableStringify(value), 'utf8');
}

export function digestData(value) {
  return crypto.createHash('sha256').update(canonicalBytes(value)).digest('hex');
}

export function loadJson(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

export function sha256File(p) {
  return crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
}

export function projectRoot() {
  return path.resolve(path.dirname(new URL(import.meta.url).pathname), '../..');
}

export function sortUnique(arr) {
  return [...new Set(arr)].sort();
}
