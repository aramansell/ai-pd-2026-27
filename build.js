#!/usr/bin/env node
/*
 * Build script for the AI-in-Education PD site.
 *
 * This assembles the site from shared sources of truth:
 *   - src/_includes/header.html and footer.html  -> the one header/nav/footer used on every page
 *   - src/data/tools.json                        -> the data for the Tools and Plans tables
 *
 * For every page it:
 *   1. Replaces the shared site header (with the correct "active" nav link and
 *      relative hrefs computed for that page's location).
 *   2. Replaces the shared site footer (same way).
 *   3. Regenerates the Tools / Plans tables from src/data/tools.json between the
 *      <!-- TABLE:... --> markers.
 *   4. Writes the result in place AND to ./dist, then copies the rest of the
 *      static site into dist/ and adds a .nojekyll marker.
 *
 * Editing the shared header, footer, or any tool table means editing ONE file
 * (a template or tools.json) and rebuilding, instead of hand-editing 12 pages.
 *
 * Run:   npm run build
 * Watch: npm run dev
 */
"use strict";

const fs = require("fs");
const path = require("path");

const SRC = __dirname;
const DIST = path.join(SRC, "dist");
const INC = path.join(SRC, "src", "_includes");
const DATA = path.join(SRC, "src", "data");

const EXCLUDE_DIRS = new Set(["node_modules", "dist", ".git", ".github", "src"]);
const EXCLUDE_FILES = new Set([
  ".DS_Store",
  "package.json",
  "package-lock.json",
  "build.js",
  ".gitignore",
]);

// ---- Shared navigation ------------------------------------------------------
const NAV = [
  { target: "index.html", label: "Home" },
  { target: "pages/pd-overview.html", label: "The 3 PD Sessions" },
  { target: "pages/tools.html", label: "AI Toolbox" },
  { target: "pages/plans.html", label: "Free vs Paid Plans" },
  { target: "pages/policies.html", label: "Policies &amp; Templates" },
  { target: "pages/department-activities.html", label: "Department Activities" },
  { target: "pages/resources.html", label: "Resources" },
];
const FOOTER_PD = [
  { target: "pages/pd-overview.html", label: "Overview &amp; Schedule" },
  { target: "pages/pd1-teachers-tools.html", label: "1 · AI for Your Daily Work" },
  { target: "pages/pd2-classroom.html", label: "2 · AI With Students" },
  { target: "pages/pd3-teaching-ai.html", label: "3 · Teaching Students AI" },
];
const FOOTER_REF = [
  { target: "pages/tools.html", label: "AI Toolbox" },
  { target: "pages/plans.html", label: "Free vs Paid Plans" },
  { target: "https://www.pps.net/departments/office-of-teaching-learning/artificial-intelligence-in-pps/ai-guidebook", label: "PPS AI Guidebook", external: true },
  { target: "pages/policies.html", label: "Policies &amp; Templates" },
  { target: "pages/privacy.html", label: "Privacy &amp; Student Data" },
];

function relHref(dir, target) {
  if (/^https?:\/\//.test(target)) return target;
  return path.posix.relative(dir || ".", target);
}

// ---- Table rendering ---------------------------------------------------------
function cellFrom(v) {
  if (typeof v === "string") return v;
  let s = '<span class="tag tag-' + v.tag + '">' + v.label + "</span>";
  if (v.suffix) s += " " + v.suffix;
  return s;
}
function toolsRow(row, withSD) {
  return (
    " <tr>\n" +
    " <td><strong>" + row.tool + "</strong></td>\n" +
    " <td>" + row.desc + "</td>\n" +
    " <td>" + row.goodFor + "</td>\n" +
    (withSD ? " <td>" + cellFrom(row.studentData) + "</td>\n" : "") +
    " <td>" + cellFrom(row.cost) + "</td>\n" +
    " <td>" + cellFrom(row.district) + "</td>\n" +
    " </tr>"
  );
}
function plansRow(row) {
  return (
    " <tr>\n" +
    " <td><strong>" + row.tool + "</strong></td>\n" +
    " <td>" + row.free + "</td>\n" +
    " <td>" + row.school + "</td>\n" +
    " <td>" + row.paid + "</td>\n" +
    " <td>" + cellFrom(row.safe) + "</td>\n" +
    " <td>" + row.notes + "</td>\n" +
    " <td>" + cellFrom(row.district) + "</td>\n" +
    " </tr>"
  );
}
function tableRows(data) {
  const pps = data.ppsApproved.map((r) => toolsRow(r, true)).join("\n");
  const other = data.other.map((r) => toolsRow(r, false)).join("\n");
  const plans = data.plans.map(plansRow).join("\n");
  return {
    "pps-approved": pps,
    other: other,
    plans: plans,
  };
}

// ---- Page transform ----------------------------------------------------------
function replaceBlock(html, openTag, closeTag, replacement) {
  const s = html.indexOf(openTag);
  if (s < 0) return { html, ok: false };
  const e = html.indexOf(closeTag, s);
  if (e < 0) return { html, ok: false };
  return { html: html.slice(0, s) + replacement + html.slice(e + closeTag.length), ok: true };
}

function replaceTable(html, id, rowsHtml) {
  const open = "<!-- TABLE:" + id + " -->";
  const close = "<!-- /TABLE:" + id + " -->";
  const s = html.indexOf(open);
  if (s < 0) { console.warn("  ! missing marker:", id); return { html, ok: false }; }
  const e = html.indexOf(close, s);
  if (e < 0) { console.warn("  ! missing end marker:", id); return { html, ok: false }; }
  const block = "\n " + open + "\n" + rowsHtml + "\n " + close + "\n";
  return { html: html.slice(0, s) + block + html.slice(e + close.length), ok: true };
}

function transform(html, pageRel, headerTpl, footerTpl, rows) {
  const dir = path.posix.dirname(pageRel) === "." ? "." : path.posix.dirname(pageRel);
  const brand = relHref(dir, "index.html");
  const navHtml = NAV.map((item) => {
    const href = relHref(dir, item.target);
    const active = pageRel === item.target ? ' class="active"' : "";
    return " <a href=\"" + href + "\"" + active + ">" + item.label + "</a>";
  }).join("\n");
  const pdHtml = FOOTER_PD.map((item) => " <li><a href=\"" + relHref(dir, item.target) + "\">" + item.label + "</a></li>").join("\n");
  const refHtml = FOOTER_REF.map((item) => {
    const ext = item.external;
    const href = ext ? item.target : relHref(dir, item.target);
    const extra = ext ? ' target="_blank" rel="noopener"' : "";
    return " <li><a href=\"" + href + "\"" + extra + ">" + item.label + "</a></li>";
  }).join("\n");

  let headerHtml = headerTpl.replace(/\{\{BRAND\}\}/g, brand).replace(/\{\{NAV\}\}/g, navHtml);
  let footerHtml = footerTpl.replace(/\{\{FOOTER_PD\}\}/g, pdHtml).replace(/\{\{FOOTER_REF\}\}/g, refHtml);

  let out = html;
  out = replaceBlock(out, '<header class="site-header">', "</header>", headerHtml).html;
  out = replaceBlock(out, '<footer class="site-footer">', "</footer>", footerHtml).html;
  // Regenerate only the tables each page is expected to carry.
  const tableIds = pageRel === "pages/tools.html" ? ["pps-approved", "other"]
    : pageRel === "pages/plans.html" ? ["plans"]
    : [];
  for (const id of tableIds) {
    out = replaceTable(out, id, rows[id]).html;
  }
  return out;
}

// ---- Build -------------------------------------------------------------------
function copyTree(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  let count = 0;
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, entry.name);
    const d = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      if (EXCLUDE_DIRS.has(entry.name)) continue;
      count += copyTree(s, d);
    } else if (entry.isFile()) {
      if (EXCLUDE_FILES.has(entry.name)) continue;
      fs.copyFileSync(s, d);
      count++;
    }
  }
  return count;
}

function htmlFiles(dir, base, out) {
  out = out || [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name.startsWith(".")) continue;
    const full = path.join(dir, entry.name);
    const rel = path.posix.join(base, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === "node_modules" || entry.name === "dist" || entry.name === "src") continue;
      htmlFiles(full, rel, out);
    } else if (entry.isFile() && entry.name.endsWith(".html")) {
      out.push({ full, rel });
    }
  }
  return out;
}

function build() {
  console.log("Building site -> dist/ ...");

  const headerTpl = fs.readFileSync(path.join(INC, "header.html"), "utf8");
  const footerTpl = fs.readFileSync(path.join(INC, "footer.html"), "utf8");
  const data = JSON.parse(fs.readFileSync(path.join(DATA, "tools.json"), "utf8"));
  const rows = tableRows(data);

  // Fresh copy of static assets into dist
  fs.rmSync(DIST, { recursive: true, force: true });
  copyTree(SRC, DIST);

  let pages = 0, missing = 0;
  for (const { full, rel } of htmlFiles(SRC, "", [])) {
    const original = fs.readFileSync(full, "utf8");
    const transformed = transform(original, rel, headerTpl, footerTpl, rows);
    const distFull = path.join(DIST, rel);
    fs.mkdirSync(path.dirname(distFull), { recursive: true });
    fs.writeFileSync(full, transformed);   // in place, so source stays openable
    fs.writeFileSync(distFull, transformed);
    pages++;
  }

  fs.writeFileSync(path.join(DIST, ".nojekyll"), "");
  console.log("  regenerated", pages, "pages (header/footer/tables)");
  console.log("  note: shared header, footer, and tool tables now come from src/_includes and src/data");
  if (missing) console.warn("  !", missing, "marker(s) not found");
  console.log("Build complete.");
}

function watch() {
  console.log("Watching for changes. Rebuilding on save (Ctrl+C to stop).");
  let timer = null;
  const onChange = () => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      try { build(); } catch (e) { console.error("Build failed:", e.message); }
    }, 200);
  };
  fs.watch(SRC, { recursive: true }, onChange);
}

if (process.argv.includes("--watch")) watch();
else build();
