# Test evidence — content release 0.5.0

47 automated tests passed: 27 Node engine/service-worker tests and 20 Python content, owner HTTP, extraction, export and source-library tests. Build passed; all 700 assets passed SHA-256 and inclusion validation. The 3,020 original records have 3,020 distinct prompt/context/option combinations.

Source preservation tests check original byte hashes, complete PDF page counts and every rendered page. Associated guides receive the same checks. Full source documents are not counted as structured scored question records. Reading-exercise tests confirm complete original context is retained. EPUB tests validate all 36 containers/chapter XML and truthful partial labels; PDF tests cover 18 original tests and answer guides; exports are reproducible.

Engine tests cover all 18 subject/form combinations, genuine/original source separation, deterministic nonduplicate grouped selection, linked-part preservation, objective/matching grading, pending written marking, exact self-marking increments, unanswered possible marks and actual-result recommendations. The first genuine Mathematics selection has source-hash/marks/grouping/calculation tests. Held source ambiguities remain excluded.

Owner tests cover anonymous rejection, sessions, CSRF and cross-origin rejection. Document-pipeline tests cover text/layout/page extraction and draft review status. A source guide downloaded from an archive is not automatically described as an official NECTA scheme or a verified scoring key.

Worker tests simulate fetch/CacheStorage for validated setup, interrupted download, quota failure, corrupted assets, refusal to activate incomplete content and retention of the previous release. These are unit simulations, not browser acceptance. No physical Android or real-browser offline workflow has been performed; no CUA browser tool is mounted. Migration/storage eviction/full interrupted-update acceptance remain outstanding.

The release-readiness gate fails as expected: detailed curriculum/cohort verification, complete books, authentic structured-bank target and browser/Android/migration acceptance remain incomplete. Original question count now exceeds 3,000, including 1,009 explicitly labelled parameterised numerical drills. The gate does not certify books merely from that count.

Packaging generates the full student web ZIP and a separate original-book/revision-paper ZIP; SHA256SUMS records their hashes. Large generated ZIPs are local/CI artifacts, not Git source. The full student bundle includes all complete source PDFs and page images. Owner-private Sites publication uses the exact committed source and its built archive.
