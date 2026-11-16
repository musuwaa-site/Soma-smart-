# Test evidence — development edition

`npm test`: 18 Node tests and 10 Python tests passed (28 total). Owner HTTP tests require socket permission; they were rerun with authorized environment escalation after sandbox socket creation failed. No approval rejection occurred.

Covered: populated 18-combination starter inventory; source eligibility; deterministic, nonduplicate grouped selection; group preservation across topic filters; objective/matching grading; written-answer pending state; permitted self-marking increments; unanswered possible marks; result-derived recommendations; missing media; duplicate/uncleared import validation; PDF text/layout/page rendering and review-state retention; anonymous admin rejection; authenticated owner content access; CSRF and cross-origin protection.

Service-worker tests run the real worker template against simulated CacheStorage/fetch events. Covered: successful integrity-checked setup; interrupted download; quota failure; corrupted content; ready-status integrity checks; refusal to activate missing content; preservation of the preceding release. These are unit simulations, **not browser offline acceptance tests**.

`npm run build`: passed. `node scripts/verify_release.mjs`: passed; all 10 required bundled student assets match SHA-256 hashes; all published diagram references are present. `npm run release-check`: intentionally fails on actual missing content/verification targets.

Not tested: real browser navigation and IndexedDB persistence, browser installation, Android storage eviction, physical Android, complete offline acceptance scenario, migration from a prior schema, and interrupted browser-controlled upgrades. The managed environment has no CUA browser tool, so no browser session was started. No browser/Android acceptance claim is made.

PDF extraction: official documents and actual archive PDFs were downloaded and processed. Watermark-only native text initially masked scanned pages; scan detection was corrected to trigger OCR on low-diversity native text. The corrected pipeline retains native text, OCR text, image renders and warnings. OCR/transcription remains unverified and unsuitable for student publication without review.
