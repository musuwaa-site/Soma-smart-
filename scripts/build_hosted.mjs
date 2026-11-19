/** Derive the private Sites package from the verified full offline build. */
import { cpSync, existsSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { writeOfflineManifest } from "./offline-manifest.mjs";

const data = JSON.parse(readFileSync("dist/library.json"));
const routes = {};
for (const doc of data.sourceDocuments) {
  for (const resource of [doc, doc.answerGuide].filter(Boolean)) {
    if (!existsSync("dist" + resource.sourcePdf) || resource.pageImages.length !== resource.pageCount)
      throw Error("Incomplete source in full build: " + resource.id);
    const source = new URL(resource.sourceReference);
    if (source.protocol !== "https:") throw Error("Expected a secure original source for " + resource.id);
    routes[resource.sourcePdf] = `#/paper-pages/${doc.id}/1${resource === doc ? "" : "/answers"}`;
    delete resource.sourcePdf;
  }
}

rmSync("dist-hosted", { recursive: true, force: true });
cpSync("dist", "dist-hosted", {
  recursive: true,
  filter: path => !Object.hasOwn(routes, path.slice("dist".length)),
});
// Keep source links in scored questions and answer guides usable without a connection.
data.sourceReaderRoutes = routes;
writeFileSync("dist-hosted/library.json", JSON.stringify(data, (_, value) =>
  typeof value === "string" && Object.hasOwn(routes, value) ? routes[value] : value, 2));
writeOfflineManifest("dist-hosted");
