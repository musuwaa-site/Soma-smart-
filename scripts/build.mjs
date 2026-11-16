import { execFileSync } from "node:child_process";
import {
  readFileSync,
  writeFileSync,
  readdirSync,
  statSync,
  copyFileSync,
} from "node:fs";
import { createHash } from "node:crypto";
execFileSync("python", ["scripts/validate.py"], { stdio: "inherit" });
execFileSync("node", ["node_modules/vite/bin/vite.js", "build"], {
  stdio: "inherit",
});
copyFileSync("content/library.json", "dist/library.json");
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
