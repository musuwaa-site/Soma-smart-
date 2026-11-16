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
  "embedded question parts. This does not certify syllabus completeness or browser behaviour.",
);
