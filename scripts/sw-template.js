const VERSION = __VERSION__,
  ASSETS = __ASSETS__,
  CACHE = "somasmart-" + VERSION;
async function broadcast(message) {
  for (const c of await self.clients.matchAll({ includeUncontrolled: true }))
    c.postMessage(message);
}
async function digest(response) {
  return [
    ...new Uint8Array(
      await crypto.subtle.digest("SHA-256", await response.arrayBuffer()),
    ),
  ]
    .map((v) => v.toString(16).padStart(2, "0"))
    .join("");
}
async function valid(cache) {
  for (const asset of ASSETS) {
    const response = await cache.match(asset.url);
    if (!response || (await digest(response)) !== asset.sha256) return false;
  }
  return true;
}
self.addEventListener("install", (event) =>
  event.waitUntil(
    (async () => {
      const cache = await caches.open(CACHE);
      let done = 0;
      try {
        // Limit concurrent requests on phones while avoiding a round trip per page.
        let next = 0;
        let failure;
        async function installAssets() {
          while (!failure && next < ASSETS.length) {
            const asset = ASSETS[next++];
            try {
              const existing = await cache.match(asset.url);
              if (!existing || (await digest(existing)) !== asset.sha256) {
                const response = await fetch(asset.url, { cache: "no-store" });
                if (!response.ok || (await digest(response.clone())) !== asset.sha256)
                  throw Error("Missing or corrupted asset: " + asset.url);
                await cache.put(asset.url, response);
              }
              await broadcast({ type: "PROGRESS", done: ++done, total: ASSETS.length });
            } catch (error) {
              failure = error;
            }
          }
        }
        await Promise.all(Array.from({length: Math.min(6, ASSETS.length)}, installAssets));
        if (failure) throw failure;
        if (!(await valid(cache)))
          throw Error("Offline content validation failed");
        await self.skipWaiting();
      } catch (e) {
        await broadcast({
          type: "ERROR",
          message:
            e.name === "QuotaExceededError"
              ? "Not enough storage. Free space and retry."
              : e.message,
        });
        throw e;
      }
    })(),
  ),
);
self.addEventListener("activate", (event) =>
  event.waitUntil(
    (async () => {
      const cache = await caches.open(CACHE);
      if (!(await valid(cache)))
        throw Error("Refusing incomplete offline release");
      await self.clients.claim(); // Older complete versions remain available for rollback; never clear student IndexedDB.
      await broadcast({ type: "READY", version: VERSION });
    })(),
  ),
);
self.addEventListener("message", (event) => {
  if (event.data.type === "STATUS")
    event.waitUntil(
      (async () => {
        const ready = await valid(await caches.open(CACHE));
        event.ports[0]?.postMessage({ ready, version: VERSION });
      })(),
    );
});
self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  if (event.request.method !== "GET" || url.origin !== self.location.origin)
    return;
  event.respondWith(
    (async () => {
      const cache = await caches.open(CACHE);
      if (event.request.mode === "navigate")
        return (await cache.match("/index.html")) || fetch(event.request);
      const asset = ASSETS.find((a) => a.url === url.pathname);
      if (asset) {
        const response = await cache.match(asset.url);
        if (response && (await digest(response.clone())) === asset.sha256)
          return response;
        const fresh = await fetch(event.request);
        if (!fresh.ok || (await digest(fresh.clone())) !== asset.sha256)
          throw Error("Asset integrity failure");
        await cache.put(asset.url, fresh.clone());
        return fresh;
      }
      return fetch(event.request);
    })(),
  );
});
