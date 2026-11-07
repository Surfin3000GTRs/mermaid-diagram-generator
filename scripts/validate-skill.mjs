import { execFileSync } from 'node:child_process';
import { readFile } from 'node:fs/promises';
import { JSDOM } from 'jsdom';
import { parse as parseYaml } from 'yaml';

const root = new URL('../', import.meta.url);
const skillDir = new URL('skills/mermaid-diagram-generator/', root);
const files = ['SKILL.md', 'SKILL.ja.md', 'references/diagram-families.md', 'references/flowchart-shapes.md'];
const texts = await Promise.all(files.map(async (file) =>
  (await readFile(new URL(file, skillDir), 'utf8')).replaceAll('\r\n', '\n')));

function frontmatter(text, file) {
  const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/);
  if (!match) throw new Error(`${file}: missing frontmatter`);
  const data = parseYaml(match[1]);
  if (data?.name !== 'mermaid-diagram-generator' || typeof data.description !== 'string' || !data.description.trim()) {
    throw new Error(`${file}: invalid name or description`);
  }
}

function headings(text) {
  return [...text.matchAll(/^(#{1,6})\s+.+$/gm)].map((match) => match[1].length);
}

function fences(text) {
  return [...text.matchAll(/^```([^\r\n]*)\r?\n([\s\S]*?)^```\s*$/gm)]
    .map((match) => ({ language: match[1].trim(), code: match[2].trim() }));
}

frontmatter(texts[0], files[0]);
frontmatter(texts[1], files[1]);
if (JSON.stringify(headings(texts[0])) !== JSON.stringify(headings(texts[1]))) {
  throw new Error('English and Japanese skill headings have different structures');
}
if (JSON.stringify(fences(texts[0])) !== JSON.stringify(fences(texts[1]))) {
  throw new Error('English and Japanese skill code fences differ');
}

const dom = new JSDOM('<!doctype html><html><body></body></html>');
globalThis.window = dom.window;
globalThis.document = dom.window.document;
Object.defineProperty(globalThis, 'navigator', { value: dom.window.navigator, configurable: true });
const { default: mermaid } = await import('mermaid');
mermaid.initialize({ startOnLoad: false });
for (let index = 0; index < files.length; index++) {
  for (const fence of fences(texts[index])) {
    if (fence.language !== 'mermaid') continue;
    try {
      await mermaid.parse(fence.code);
    } catch (error) {
      throw new Error(`${files[index]}: invalid Mermaid example`, { cause: error });
    }
  }
}
const tracked = (await readFile(new URL('.github/mermaid-version.txt', root), 'utf8')).trim();
const installed = JSON.parse(await readFile(new URL('node_modules/mermaid/package.json', root), 'utf8')).version;
if (tracked !== installed) throw new Error(`Tracked Mermaid ${tracked} does not match parser ${installed}`);
execFileSync('python', ['scripts/watch_mermaid.py', '--check-catalog'], { cwd: root, stdio: 'inherit' });
console.log(`Validated skill frontmatter, translations and Mermaid ${installed} examples.`);
