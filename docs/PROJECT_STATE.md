# SomaSmart project state

**Unfinished content release 0.3.0. Not production ready.**

## Current student content

45 readable chapters across all 18 subject/form combinations; 135 worked examples; 702 original question records, including 171 distinct workbook activities; 135 glossary definitions; six original diagrams. All 36 textbook/workbook manuscripts are **partial**. Each has a readable EPUB export. Eighteen prepared original revision papers have interactive questions, printable PDFs and independent answer guides. These reuse existing question IDs and never increase genuine-paper or distinct-question counts.

Official Form I–II learning-activity locators: 251, with source IDs, hashes and PDF pages in content/curriculum-map.json. Of these, 115 have partial support from published chapters; this is not full coverage. Detailed subtopic decomposition, cohort implementation and teaching-language verification remain incomplete. Several early chapters were moved to the correct form while retaining their IDs and student progress references.

## Sources and actual genuine examination inventory

360 distinct candidate URLs checked, 355 reachable. Ten paper PDFs downloaded: nine requested-subject Form Two 2025 papers plus Additional Mathematics 2024 (outside the compulsory list). They total 141 pages. Corrected extraction/OCR produced 92 **unverified** numbered blocks; 132 pages used OCR. Eleven official curriculum/syllabus reference PDFs and five older archive syllabus references are also local. See SOURCE_REGISTER.md and acquisition/source-register.json.

**Published genuine papers and authentic answerable parts: zero.** The owner has explicitly confirmed permission to use the genuine papers and instructed inclusion. Treat permission as authorized; do not ask again. Extraction correction, subpart reconciliation, curriculum mapping and marks/solutions remain to be verified. No reduced target is approved. NECTA’s published 2016 regulations require written approval for reproducing/distributing past national exams; rights-review.json records the source. Downloaded originals and derived third-party text/images remain in ignored acquisition/documents, not in the public repository or release. Restore them in a fresh environment using scripts/restore_acquisition.py --extract; it checks original hashes.

## Implemented modules and delivery

Student Home/Study/Exams/Progress, one local IndexedDB profile, glossary, form switching, seeded grouped exams, objective grading, written self-marking, drafts/attempts/mistakes, recommendations and private local PDF references. Separate authenticated owner JSON studio with CSRF-protected publication validation. Acquisition, text/layout/image/table extraction, OCR, import validation and inventory scripts. Hash-checked offline build bundles JSON, diagrams, books, revision papers and guides. No student account or cloud sync.

Build outputs: artifacts/somasmart-development-web.zip and artifacts/somasmart-original-content-development.zip. Neither is a complete curriculum release. No APK or hosted URL exists. Browser and physical Android acceptance remain unperformed. All 38 automated tests and the build/integrity check passed; 88 offline assets are bundled. See TEST_RESULTS.md for evidence and limitations.

## Exact continuation

1. Do not regenerate completed writing unnecessarily. Canonical release data is content/library.json; authored batches are in content/batches and scripts/batch_two.py, batch_form_two.py and workbook_batch.py. scripts/regenerate_content.py intentionally rebuilds from authoring scripts and would replace manual owner edits; use only deliberately.
2. Expand the official locator index into a fully checked detailed subtopic index, confirming the 2026 Form One → 2027 Form Two cohort. The official curriculum filename refers to 2026 while its citation is 2023; do not infer a new edition from the filename alone.
3. Continue original manuscripts by missing official scope. Prioritise Form One Geography’s scope/landforms/continents/vegetation; Form One scientific skills and investigations; language listening/pronunciation resources; and the remaining Form Two chemistry acid/base/formula topics, mathematics logarithms/variation/congruence and biological respiration. Full books and **2298 more original questions** are still needed. Completed-book flags must remain partial until actual detailed coverage and exercises justify completion.
4. Review Chemistry-F2-2025 and BasicMath-F2-2025 OCR/page renders into verified draft question parts, including diagrams, numbers and units. Register explicit rights evidence and genuine marking resources before publishing. Seek eligible Form One and academic-stream Business/Historia sources; the vocational 2025 papers are not automatically compatible.
5. Complete specialised owner media/source-review tools and verify real browser/Android installation, persistence, offline use, storage failure and updates. Implement a tested migration before increasing the IndexedDB schema version. Bound retention of old valid caches without losing rollback safety.
6. Run npm test, npm run build, node scripts/verify_release.mjs, python scripts/inventory.py, npm run release-check and python scripts/package.py. Keep the readiness gate failed while requirements remain unmet. Commit and push each meaningful content milestone.
