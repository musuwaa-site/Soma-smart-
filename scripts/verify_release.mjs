import { readFileSync, existsSync } from "node:fs";
import { createHash } from "node:crypto";
const manifest = JSON.parse(readFileSync("dist/release.json"));
for (const a of manifest.assets) {
  const path = "dist" + a.url;
  if (!existsSync(path)) throw Error("Missing offline asset " + a.url);
  const sha = createHash("sha256").update(readFileSync(path)).digest("hex");
  if (sha !== a.sha256) throw Error("Corrupted offline asset " + a.url);
}
const data = JSON.parse(readFileSync("dist/library.json"));
if(data.questions.some(q=>q.publicationStatus!=='published') || data.sourceDocuments.some(d=>d.publicationStatus!=='published'))throw Error('Unpublished source content leaked into student release');
for (const l of data.lessons)
  if (l.diagram && !manifest.assets.some((a) => a.url === l.diagram))
    throw Error("Unbundled diagram: " + l.diagram);
for (const q of data.questions)
  for (const m of q.media)
    if (!manifest.assets.some((a) => a.url === m.path))
      throw Error("Unbundled question media " + m.path);
console.log(
  "Offline package integrity passed:",
  manifest.assets.length,
  "assets;",
  data.lessons.length,
  "readable chapters;",
  data.questions.length,
  "embedded question records. This does not certify syllabus completeness or browser behaviour.",
);
for (const b of data.books) {
  const path = '/books/' + b.id + '.epub';
  if (!manifest.assets.some(a => a.url === path)) throw Error('Unbundled book: ' + path);
}
for (const p of data.papers.filter(p => p.sourceType === 'original' && p.publicationStatus === 'published')) {
  for (const suffix of ['.pdf','-answers.pdf']) {
    const path = '/exams/' + p.id + suffix;
    if (!manifest.assets.some(a => a.url === path)) throw Error('Unbundled revision paper: ' + path);
  }
}
for (const d of data.sourceDocuments || []) {
  for (const resource of [d, d.answerGuide].filter(Boolean)) {
    const actual = createHash('sha256').update(readFileSync('dist' + resource.sourcePdf)).digest('hex');
    if (actual !== resource.sha256) throw Error('Archived PDF bytes changed: ' + resource.sourcePdf);
  }
  for (const path of [d.sourcePdf,...d.pageImages,...(d.answerGuide?[d.answerGuide.sourcePdf,...d.answerGuide.pageImages]:[])]) {
    if (!manifest.assets.some(a=>a.url===path)) throw Error('Unbundled complete paper asset: '+path);
  }
}

const withoutInteractive = data.sourceDocuments.filter(doc => !doc.interactivePaperId && !doc.practiceIndex);
if (withoutInteractive.length) throw Error('Source papers missing interactive practice: ' + withoutInteractive.map(doc=>doc.id).join(', '));
