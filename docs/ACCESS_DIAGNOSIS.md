# Site access diagnosis — 16 November 2026

User reports “This site can’t be reached”. The exact browser error code is not yet available. This remains distinct from an application blank screen; do not claim the user’s connection is repaired without confirmation.

Confirmed: public DNS resolves the existing Site hostname; Sites reports active owner-private access and successful deployment. Owner-authorized HTTP checks returned 200 for the page, bundled JavaScript/CSS, library JSON, manifest and service worker. No runtime-error events were returned. Unauthenticated automated requests saw Cloudflare 1010; a request without valid owner sign-in sees 401. Those observations do not establish which error the user’s browser receives. Audience was not changed.

A real startup weakness was identified: index.html contained an empty app container while the approximately 8 MB library downloaded. The hosting screenshot was blank. The fix adds an immediate visible startup screen, streamed download progress, clear authentication/network/content errors, a 45-second stalled-network timeout and a 15-second storage-wait timeout. Recovery does not clear student data. Failed script loading also shows recovery text rather than leaving an empty screen.

Six new regression tests cover streamed Unicode data/progress, 401/403 responses, HTML returned instead of JSON, stalled connections, failed/malformed data and unresponsive local storage. Total 64 automated tests pass. The complete 689-asset offline build passes integrity checks. Content totals are unchanged.

Real-browser/CUA tools are absent from this task even though desktop capability is enabled on demand. Browser/Android flow verification remains unavailable. After publishing, repeat the authenticated HTTP checks. If the user still cannot connect, obtain the exact browser error code and whether the link opens inside ChatGPT or a signed-in external browser. Do not make the private site public or erase student storage as a speculative fix.
