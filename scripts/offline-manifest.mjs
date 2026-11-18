import { readFileSync, readdirSync, statSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";

export function writeOfflineManifest(directory) {
  const files = (p) =>
    readdirSync(p).flatMap((n) =>
      statSync(`${p}/${n}`).isDirectory() ? files(`${p}/${n}`) : [`${p}/${n}`],
    );
  const assets = files(directory)
    .filter((p) => !p.endsWith("/sw.js") && !p.endsWith("/release.json"))
    .map((p) => ({
      url: p.slice(directory.length),
      sha256: createHash("sha256").update(readFileSync(p)).digest("hex"),
    }));
  const version = createHash("sha256")
    .update(JSON.stringify(assets))
    .digest("hex")
    .slice(0, 16);
  const template = readFileSync("scripts/sw-template.js", "utf8");
  writeFileSync(
    `${directory}/sw.js`,
    template
      .replace("__VERSION__", JSON.stringify(version))
      .replace("__ASSETS__", JSON.stringify(assets)),
  );
  writeFileSync(
    `${directory}/release.json`,
    JSON.stringify({ version, assets }, null, 2),
  );
  console.log(
    `Offline release ${version}: ${assets.length} integrity-checked assets`,
  );
}
