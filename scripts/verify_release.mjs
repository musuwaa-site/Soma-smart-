import { readFileSync, existsSync, statSync } from "node:fs";
import { createHash } from "node:crypto";

const hosted = process.argv.includes("--hosted");
const directory = hosted ? "dist-hosted" : "dist";
const manifest = JSON.parse(readFileSync(directory + "/release.json"));
const paths = new Set(manifest.assets.map(asset => asset.url));
function requireAsset(path) {
  if (!paths.has(path)) throw Error("Unbundled offline asset: " + path);
}
let bytes = statSync(directory + "/release.json").size + statSync(directory + "/sw.js").size;
for (const asset of manifest.assets) {
  const path = directory + asset.url;
  const contents = readFileSync(path);
  bytes += contents.length;
  if (createHash("sha256").update(contents).digest("hex") !== asset.sha256)
    throw Error("Corrupted offline asset: " + asset.url);
}
if (hosted && bytes + statSync(".openai/hosting.json").size >= 256 * 1024 ** 2)
  throw Error("Hosted release exceeds the Sites archive size limit.");
const data = JSON.parse(readFileSync(directory + "/library.json"));
if (data.questions.some(q => q.publicationStatus !== "published") ||
    data.sourceDocuments.some(d => d.publicationStatus !== "published"))
  throw Error("Unpublished content in student release");
for (const lesson of data.lessons) if (lesson.diagram) requireAsset(lesson.diagram);
for (const question of data.questions) for (const media of question.media) requireAsset(media.path);
for (const book of data.books) requireAsset("/books/" + book.id + ".epub");
for (const paper of data.papers.filter(p => p.sourceType === "original" && p.publicationStatus === "published"))
  for (const suffix of [".pdf", "-answers.pdf"]) requireAsset("/exams/" + paper.id + suffix);

for (const doc of data.sourceDocuments) {
  if (!doc.interactivePaperId && !doc.practiceIndex) throw Error("Missing interactive practice: " + doc.id);
  for (const resource of [doc, doc.answerGuide].filter(Boolean)) {
    if (!resource.pageCount || resource.pageImages.length !== resource.pageCount)
      throw Error("Original pages missing: " + resource.id);
    resource.pageImages.forEach(requireAsset);
    if (!hosted) {
      requireAsset(resource.sourcePdf);
      const hash = createHash("sha256").update(readFileSync(directory + resource.sourcePdf)).digest("hex");
      if (hash !== resource.sha256) throw Error("Archived PDF bytes changed: " + resource.id);
    } else {
      if (resource.sourcePdf || new URL(resource.sourceReference).protocol !== "https:")
        throw Error("Incorrect hosted PDF source link: " + resource.id);
    }
  }
}
if (hosted) {
  const full = JSON.parse(readFileSync("dist/library.json"));
  for (const doc of full.sourceDocuments) {
    const copy = data.sourceDocuments.find(paper => paper.id === doc.id);
    if (!copy) throw Error("Hosted paper missing: " + doc.id);
    for (const resource of [doc, doc.answerGuide].filter(Boolean)) {
      const hostedResource = resource === doc ? copy : copy.answerGuide;
      const route = `#/paper-pages/${doc.id}/1${resource === doc ? "" : "/answers"}`;
      if (data.sourceReaderRoutes[resource.sourcePdf] !== route || existsSync(directory + resource.sourcePdf) ||
          JSON.stringify(hostedResource?.pageImages) !== JSON.stringify(resource.pageImages))
        throw Error("Hosted reader and full archive disagree: " + resource.id);
    }
  }
}
console.log(`Verified ${directory}: ${manifest.assets.length} offline assets, ${data.sourceDocuments.length} interactive source papers (${(bytes/1024**2).toFixed(1)} MiB).`);
