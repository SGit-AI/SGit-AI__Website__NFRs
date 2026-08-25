#!/usr/bin/env node
// nfrs.sgit.ai pre-release gate. Run from anywhere: node admin/build/validate.js
// Checks, in order:
//   1. version agreement — admin/build/version.txt vs every page's version badge,
//      the versions table, llms.txt, llms-full.txt and index.md
//   2. internal links — every relative href/src in every .html file resolves to a
//      file in the tree (fragments stripped; external and mailto links skipped)
//   3. canonical host — every <link rel="canonical"> and og:url points at the host
//      in CNAME. This site links out to twelve siblings, so a canonical left
//      pointing at a sibling host is the specific mistake worth catching in CI.
//   4. key-leak tripwire — nothing in the tree may look like an sgit vault key
//      (a >=20-char passphrase joined by a colon to a uuid-shaped id).
//   5. the hub's own rule — every page carrying a number must say where the
//      number came from. Enforced as: every discipline page links at least one
//      sibling site (link-the-measurement-never-restate-it), and every page
//      carrying a "dated" claim carries the date in a <span class="asof"> so a
//      stale figure is visible rather than silent.
// Any failure exits 1: no tag, no publish.
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const errors = [];

function walk(dir, out = []) {
  for (const name of fs.readdirSync(dir)) {
    if (name === '.git' || name === '.github' || name === 'node_modules' || name === '.sg_vault') continue;
    const p = path.join(dir, name);
    const st = fs.statSync(p);
    if (st.isDirectory()) walk(p, out);
    else out.push(p);
  }
  return out;
}

const files = walk(ROOT);
const htmlFiles = files.filter(f => f.endsWith('.html'));

// --- 1. version agreement -------------------------------------------------
const VERSION = fs.readFileSync(path.join(ROOT, 'admin/build/version.txt'), 'utf8').trim();
if (!/^v\d+\.\d+\.\d+$/.test(VERSION)) {
  errors.push(`version.txt does not carry a vX.Y.Z version: "${VERSION}"`);
}
for (const f of htmlFiles) {
  const t = fs.readFileSync(f, 'utf8');
  const badges = [...t.matchAll(/class="ver"[^>]*>(v\d+\.\d+\.\d+)</g)].map(m => m[1]);
  for (const b of badges) if (b !== VERSION) {
    errors.push(`${path.relative(ROOT, f)}: version badge ${b} != ${VERSION}`);
  }
}
for (const extra of ['llms.txt', 'llms-full.txt', 'index.md']) {
  const t = fs.readFileSync(path.join(ROOT, extra), 'utf8');
  if (!t.includes(VERSION)) errors.push(`${extra} does not mention ${VERSION}`);
}
const versTable = fs.readFileSync(path.join(ROOT, 'admin/versions.html'), 'utf8');
if (!versTable.includes(`class="vnum">${VERSION}<`)) {
  errors.push(`admin/versions.html has no row for ${VERSION}`);
}
// each release appears exactly once — a blanket version-bump sed that touches
// the history table produces duplicates, which shipped once on the NHI site
const rows = [...versTable.matchAll(/class="vnum">(v\d+\.\d+\.\d+)</g)].map(m => m[1]);
for (const v of rows) if (rows.filter(x => x === v).length > 1) {
  errors.push(`admin/versions.html lists ${v} more than once`);
  break;
}

// --- 2. internal links ----------------------------------------------------
for (const f of htmlFiles) {
  const t = fs.readFileSync(f, 'utf8');
  const dir = path.dirname(f);
  for (const m of t.matchAll(/(?:href|src)="([^"#]+)(?:#[^"]*)?"/g)) {
    const target = m[1];
    if (/^(https?:|mailto:|data:|\/\/)/.test(target) || target === '') continue;
    const resolved = path.resolve(dir, target);
    if (!fs.existsSync(resolved)) {
      errors.push(`${path.relative(ROOT, f)}: broken link -> ${target}`);
    }
  }
}

// --- 3. canonical host ----------------------------------------------------
const HOST = fs.readFileSync(path.join(ROOT, 'CNAME'), 'utf8').trim();
if (!/^[a-z0-9.-]+$/.test(HOST)) errors.push(`CNAME does not carry a hostname: "${HOST}"`);
for (const f of htmlFiles) {
  const t = fs.readFileSync(f, 'utf8');
  const claimed = [
    ...[...t.matchAll(/<link[^>]+rel="canonical"[^>]+href="([^"]+)"/g)].map(m => m[1]),
    ...[...t.matchAll(/<meta[^>]+property="og:url"[^>]+content="([^"]+)"/g)].map(m => m[1]),
  ];
  for (const url of claimed) if (!url.startsWith(`https://${HOST}/`)) {
    errors.push(`${path.relative(ROOT, f)}: canonical/og:url is not on ${HOST} -> ${url}`);
  }
  // every page must declare where it canonically lives
  if (!/rel="canonical"/.test(t)) {
    errors.push(`${path.relative(ROOT, f)}: no canonical link`);
  }
}

// --- 4. key-leak tripwire -------------------------------------------------
const KEY_SHAPE = /[A-Za-z0-9_-]{20,}:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/;
for (const f of files) {
  if (/\.(png|jpg|jpeg|gif|webp|ico|woff2?|zip)$/.test(f)) continue;
  const t = fs.readFileSync(f, 'utf8');
  if (KEY_SHAPE.test(t)) {
    errors.push(`${path.relative(ROOT, f)}: contains a vault-key-shaped string`);
  }
}

// --- 5. the hub's own rule ------------------------------------------------
// This site quotes more sibling measurements than any other in the network, so
// the rule it teaches is the rule CI enforces on it: link the measurement, never
// restate it; generate or date every number.
//
// (a) Every discipline page must carry at least one link to the sibling site
//     that owns its artefacts. A discipline page that cites nobody has either
//     re-measured (forbidden) or is asserting without provenance.
const DISCIPLINE = ['testing', 'ci', 'documentation', 'ifd', 'budgets', 'pm',
                    'resilience', 'backups', 'scorecard', 'map', 'memory'];
//     The nav and the footer must be stripped before looking. The footer's own
//     network line links three siblings on every page in the tree, so a check
//     that reads the whole file is satisfied by the chrome and can never fail —
//     which is not a check, it is a green tick with no referent. This estate
//     already shipped one guard with exactly that defect (see /testing/#counter),
//     so the mistake is worth naming in the source of the guard that avoids it.
function bodyOnly(text) {
  return text
    .replace(/<nav class="site">[\s\S]*?<\/nav>/, '')
    .replace(/<footer class="site">[\s\S]*?<\/footer>/, '')
    .replace(/<head>[\s\S]*?<\/head>/, '');
}
for (const d of DISCIPLINE) {
  const f = path.join(ROOT, d, 'index.html');
  if (!fs.existsSync(f)) { errors.push(`${d}/index.html is missing`); continue; }
  const body = bodyOnly(fs.readFileSync(f, 'utf8'));
  if (!/href="https:\/\/(?:[a-z0-9-]+\.)?sgit\.ai/.test(body)) {
    errors.push(`${d}/index.html: no link to a sibling site in the page body — the hub links the measurement, it does not restate it`);
  }
}
// (b) Every page that carries a figure must carry an as-of date beside it. The
//     marker is <span class="asof">, which the stylesheet renders visibly: a
//     number whose date is missing is a number nobody can check.
//
//     "A figure" has to be defined carefully or the check is useless in both
//     directions. Three things are NOT figures and were flagged as such by the
//     first draft of this rule: a four-digit year, a version string, and a
//     licence name (CC BY 4.0). None of them is a measurement, and treating them
//     as one trains people to add a meaningless date to silence the gate — which
//     is exactly the outcome this rule exists to prevent.
//
//     A document reader page satisfies the rule through its docmeta block, which
//     carries the source document's own date. That date is the right one for a
//     verbatim republication: the page is as fresh as the document it renders.
const YEAR = /^(?:1[89]|20)\d\d$/;
for (const f of htmlFiles) {
  const rel = path.relative(ROOT, f);
  if (rel.startsWith('admin/')) continue;      // the versions table is dated by row
  const t = fs.readFileSync(f, 'utf8');
  const dated = /class="asof"/.test(t)
             || (/class="docmeta"/.test(t) && /<span class="k">Date<\/span>/.test(t));
  if (dated) continue;
  const prose = bodyOnly(t)
    .replace(/<[^>]+>/g, ' ')                  // attributes hold paths and versions
    .replace(/\bv\d+(?:\.\d+)+/g, ' ')       // version strings
    .replace(/\bCC BY \d+(?:\.\d+)?/g, ' '); // the licence name
  const figures = (prose.match(/\d[\d,]{2,}(?:\.\d+)?|\d+(?:\.\d+)?%/g) || [])
    .filter(x => !YEAR.test(x.replace(/,/g, '')));
  if (figures.length) {
    errors.push(`${rel}: carries figures (${figures.slice(0, 3).join(', ')}) but no `
      + `<span class="asof"> date — generate or date every number`);
  }
}

// --- report ---------------------------------------------------------------
if (errors.length) {
  console.error(`validate: ${errors.length} error(s)`);
  for (const e of errors) console.error('  ✗ ' + e);
  process.exit(1);
}
console.log(`validate: OK — ${VERSION} on ${HOST}, ${htmlFiles.length} pages, links resolve, every discipline page cites a sibling, every figure dated, no key-shaped strings`);
