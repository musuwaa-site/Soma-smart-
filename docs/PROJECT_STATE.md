# SomaSmart project state

**Stage: unfinished development implementation spanning Steps 1–6. Not production ready.**

## Implemented

Vite/JavaScript student app; Home/Study/Exams/Progress routes; both forms and nine subjects; reader/workbook views; glossary and two original SVG diagrams; MCQ/matching/written/calculation/essay controls; seeded grouped exams; exact self-marking increments; one local IndexedDB profile, drafts, attempts, mistakes and recommendations; private on-device reference PDF import; separate password-authenticated owner JSON editor and publication validator; PDF acquisition/text/layout/image/table/page-render/OCR scripts; duplicate-safe reviewed-content importer; hash-checked service-worker provisioning; production-format build and ZIP packaging.

Actual content: 36 original readable chapters, 108 worked examples, 540 original questions (including 144 distinct workbook tasks), 108 glossary definitions, six original diagrams and 36 **partial** book records. Eighteen prepared original revision papers reference existing items and are counted separately from genuine papers. Zero complete textbooks/workbooks. Every combination has real readable material. Official learning-activity locators (251) are indexed with source hashes and PDF pages; 78 have partial chapter support. Detailed subtopic coverage remains incomplete. Some starter chapters were moved to the correct form while preserving their stable IDs and progress. No official subtopic coverage percentage is claimed.

Sources: 360 distinct real paper URLs received HTTP checks (355 responded). Nine requested-subject 2025 Form Two papers and one Additional Mathematics 2024 paper downloaded; the latter is outside the compulsory list. Business/Historia 2025 papers are vocational and require compatibility review. Eleven official reference PDFs acquired (nine subjects, two Kiswahili editions and the currently linked curriculum) plus five older archive syllabus references. See generated SOURCE_REGISTER.md and source-register.json for hashes and exact sources. Original third-party PDFs and extraction artifacts remain in the local ignored acquisition workspace; they are not redistributed in GitHub or the app.

Authentic published papers/questions: **0**. Rights, extraction, topic mapping, answers and marks are unverified. No reduced authentic target has been approved. The 10 paper PDFs total 141 pages; the corrected pipeline produced 92 unverified detected blocks, with OCR on 132 pages. These are draft candidates, not verified questions or source paper counts. The inventory script calculates extraction counts from actual nonempty staged detection output.

Tests: the initial 28 automated tests passed; expansion-specific checks are added in this milestone; build and offline package integrity passed. Browser/physical Android tests not run. See TEST_RESULTS.md. Owner admin runs separately and is not deployed. No APK or hosted URL exists.

## Known limitations

- Full verified official detailed subtopic index and Form Two 2027 transition are unresolved. The current official curriculum PDF filename refers to 2026 but document citation says 2023.
- Full educational manuscripts, mixed-topic workbook tests and 2460 further original practice items remain to be produced and reviewed.
- Genuine papers have not been rights-cleared or turned into verified, marked offline student records. Most require manual correction after OCR.
- Admin editing is authenticated and phone-friendly but uses JSON fields; specialised source-page/diagram editors and upload workflows remain unfinished. Publish updates source content; delivery requires rebuild/repackage.
- Student private PDFs are local reference downloads, not automatic scored examinations.
- Browser offline/progress/update and low-storage acceptance scenarios, future schema migrations, real Android testing and installation remain unverified. Cache retention currently keeps old versions and needs a bounded validated cleanup policy for long-term device storage.

## Exact continuation

1. Retain existing authored content. In a fresh environment restore ignored source originals with `python scripts/restore_acquisition.py --extract` (URL/hash verification). Use content/curriculum-map.json for 251 factual activity locators. Read downloaded official documents in acquisition/documents; expand the locator index into a manually verified detailed subtopic index for Forms I and II for all nine subjects, with edition/page and cohort implementation evidence. Resolve teaching language and edition differences. Do not reuse older History as Historia.
2. Review OCR output and page renders for Chemistry-F2-2025 and BasicMath-F2-2025 first. Reconcile page joins, numbers, subparts, figures, units and tables into draft schema records. Obtain explicit reuse clearance/open-license evidence before publication; record it. Associate verified or clearly independent solutions and marks. Then import reviewed publishable records with scripts/import_content.py.
3. Expansion sources are scripts/batch_two.py and scripts/workbook_batch.py; published increments are in content/batches. Continue expanding all 18 manuscripts/workbooks systematically by verified subtopic, aiming for 3 worked examples and 15 answered activities per subtopic and at least 3000 original questions. Update completion flags only on real coverage.
4. Acquire Form One sources and academic-stream current-curriculum Business/Historia papers; continue toward the conditional 180-paper/3000-part targets. No paper-target reduction is authorized.
5. Finish owner media/source-review tooling. Run real browser/Android workflows including persistence, private imports, interrupted provisioning/upgrades and storage failures; record evidence in content/acceptance.json only after testing. Implement and test any schema migration before a schema version bump.
6. Run npm test, npm run build, node scripts/verify_release.mjs, python scripts/inventory.py, npm run release-check. Final readiness must remain failed while mandatory gaps exist. Repackage, commit and push meaningful milestones.

## Content milestone 0.2

Imported an original chapter batch for every subject/form, distinct workbook questions, original revision papers, and four additional diagrams. All book completion flags remain partial. NECTA’s official 2016 examination regulations explicitly require written approval before past papers are reproduced/distributed; no such approval has been supplied. Reference: https://necta.go.tz/publications/Exam%20Regulations/EXAM_REGULATIONS_2016.pdf . Continue original authorship independently of that unresolved permission.
