# Test evidence — content release 0.3.0

The final verification command is `npm test`. It runs Node engine/worker tests and Python content/owner/export tests. Current expansion checks cover original-paper attribution and totals, distinct workbook activities, correct form/page curriculum references and stable IDs through form corrections. Exact final pass totals are recorded after the final run below.

Engine coverage includes: populated 18-combination inventory; source eligibility; reproducible nonduplicate grouped selection; shared-group preservation across topic filters; objective/matching grading; written-answer pending state and valid self-marking increments; unanswered possible marks and result-derived recommendations. Content validation checks missing media, duplicate IDs, false completion claims, unsafe export identifiers and falsely relabelled genuine-paper provenance.

Owner HTTP tests cover anonymous rejection, authenticated content access, CSRF enforcement and cross-origin rejection. Local socket access requires an authorized sandbox escalation; tests ran with that permission. PDF pipeline tests cover text/layout/page rendering and draft review state. Actual downloaded scans remain unverified even where OCR detected blocks.

EPUB/PDF export tests check all 36 real EPUB containers and chapter XML, truthful partial labels, nonempty original revision and answer-guide PDFs, and deterministic repeated exports. Kiswahili question-paper and Mathematics answer-guide PDF samples were visually inspected from rendered images; this is document QA, not browser testing.

Worker tests use the real worker template with simulated fetch/CacheStorage. They cover successful validated setup, interrupted download, quota failure, corrupted assets, ready-status validation, refusal to activate incomplete content and preservation of the previous release. These are unit simulations, **not browser offline acceptance**.

The production-format build and SHA-256 package validation include 88 assets: all app/content assets, diagrams, EPUB manuscripts, original revision PDFs and answer guides. No genuine past-paper text is published. The final readiness gate must fail on incomplete manuscripts, detailed curriculum verification, genuine inventory and unperformed device acceptance.

Not run: real-browser navigation, IndexedDB persistence and installation, physical Android, storage eviction, complete offline acceptance scenario, prior-version schema migration and browser-controlled interrupted upgrades. The managed environment has no CUA browser tool. No browser/Android acceptance claim is made.

Final run: **38 tests passed** (22 Node + 16 Python). Build passed. All 88 required offline assets passed hash/inclusion validation. The readiness command returned failure as expected: incomplete detailed curriculum, incomplete books, 2298 missing original questions, unresolved genuine inventory and unrun browser/Android/migration acceptance. Both delivery archives were regenerated after these checks; SHA256SUMS records their hashes.

## Private preview and first genuine selection (0.3.1)

The owner confirmed permission; it is recorded as owner attestation, not falsely described as inspection of an uploaded document. The private Site was published successfully at https://somasmart-study.astuteegret257.chatgpt.site . Source helper scripts were not mounted in this environment, so source was pushed with ordinary Git using the short-lived Sites credential only through hidden stdin and process-memory HTTP headers. The deployed archive contains the exact pushed source's hosting manifest and built dist directory.

First source review inspected all relevant Mathematics page renders, then transcribed seven whole main questions with 18 labelled parts. Tests check the source PDF hash, verified 10-mark whole-question allocation, preserved grouping, independently calculated numeric solutions, pending written marking, and exclusion of ambiguous/misordered source items. Source diagrams were also visually checked after cropping. Whole-question marks are from the paper; detailed rubric increments/weights are explicitly independent self-assessment, not an official NECTA scheme. This is a partial source selection, not a claim that all ten paper questions passed review.

Browser/Android acceptance remains unperformed. A refresh button now appears when a previously installed worker is replaced, so an already-open preview can load newly published content without discarding the locally saved profile.
