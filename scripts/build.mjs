import { execFileSync } from "node:child_process";
import {
  readFileSync,
  writeFileSync,
  readdirSync,
  statSync,
  copyFileSync,
  rmSync,
} from "node:fs";
import { createHash } from "node:crypto";
import { studentRelease } from './student-release.mjs';
execFileSync("python", ["scripts/validate.py"], { stdio: "inherit" });
execFileSync("python", ["scripts/export_books.py"], { stdio: "inherit" });
execFileSync("python", ["scripts/export_exams.py"], { stdio: "inherit" });
execFileSync("node", ["node_modules/vite/bin/vite.js", "build"], {
  stdio: "inherit",
});
const published=studentRelease(JSON.parse(readFileSync('content/library.json')));
const sourceFolders=new Set(published.sourceDocuments.flatMap(d=>[d.sourcePdf,d.answerGuide?.sourcePdf].filter(Boolean)).map(path=>path.split('/')[2]));
for(const q of published.questions)for(const m of q.media||[])if(m.path.startsWith('/source-papers/'))sourceFolders.add(m.path.split('/')[2]);
for(const folder of readdirSync('dist/source-papers'))if(!sourceFolders.has(folder))rmSync('dist/source-papers/'+folder,{recursive:true});
const previewMap = 'dist/.preview-map.json';
execFileSync('python', ['scripts/compact_source_previews.py', 'dist', previewMap], { stdio: 'inherit' });
const previewPaths = JSON.parse(readFileSync(previewMap));
rmSync(previewMap);
writeFileSync('dist/library.json', JSON.stringify(published, (_, value) =>
  typeof value === 'string' && Object.hasOwn(previewPaths, value) ? previewPaths[value] : value, 2));
const walk = (p) =>
  readdirSync(p).flatMap((n) =>
    statSync(`${p}/${n}`).isDirectory() ? walk(`${p}/${n}`) : [`${p}/${n}`],
  );
const assets = walk("dist")
  .filter((p) => !p.endsWith("sw.js"))
  .map((p) => ({
    url: "/" + p.slice(5),
    sha256: createHash("sha256").update(readFileSync(p)).digest("hex"),
  }));
const version = createHash("sha256")
  .update(JSON.stringify(assets))
  .digest("hex")
  .slice(0, 16);
const template = readFileSync("scripts/sw-template.js", "utf8");
writeFileSync(
  "dist/sw.js",
  template
    .replace("__VERSION__", JSON.stringify(version))
    .replace("__ASSETS__", JSON.stringify(assets)),
);
writeFileSync(
  "dist/release.json",
  JSON.stringify({ version, assets }, null, 2),
);
console.log(
  `Offline release ${version}: ${assets.length} integrity-checked assets`,
);
