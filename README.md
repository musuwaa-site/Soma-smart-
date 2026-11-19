# SomaSmart

**Unfinished development edition.** Offline-first educational app for Tanzania Forms One and Two. This repository contains working software and actual original starter content, not a complete curriculum release.

## Run

Requires Node 24+, Python 3.12+, and PyMuPDF (for document processing).

```sh
npm ci
python -m pip install -r requirements.txt
npm run dev
```

For the production-format offline bundle:

```sh
npm test
npm run build
node scripts/verify_release.mjs
python scripts/package.py
```

The ZIP is `artifacts/somasmart-development-web.zip`. Serve **all** of `dist/` at the root of an HTTPS static host, with SPA fallback to `index.html`; `sw.js` should use `Cache-Control: no-cache`. Localhost also supports service workers. Do not open `index.html` as a file. `npm run dev` is for development, not offline acceptance. A private ChatGPT Sites preview is available at https://somasmart-study.astuteegret257.chatgpt.site . No APK has been produced.

## Installation

Open the HTTPS site in Android Chrome to study online. Offline download starts paused. Tap **Download for offline use** to start or resume, or **Pause download** to stop. After **Library ready offline** appears, use the browser’s Install/Add to Home Screen action. Readiness checks every bundled asset, not merely the service-worker registration. If setup fails, free storage, reconnect and tap the download button to retry. Device storage eviction may require reprovisioning. Clearing site data erases progress. Android installation and physical-device behaviour remain unverified.

## Included

Home, two-form subject library, original readable starter chapters, glossary dialogs, diagrams, textbook/workbook views, objective and self-marked exam questions, seeded selection, local draft persistence, results and topic recommendations. Student data uses one IndexedDB profile without accounts or cloud sync. Content is local JSON interpreted directly by the app.

See [actual inventory](docs/CONTENT_INVENTORY.md), [project state](docs/PROJECT_STATE.md), [source register](docs/SOURCE_REGISTER.md) and [test evidence](docs/TEST_RESULTS.md). `npm run release-check` deliberately fails for this incomplete edition.

## Content processing

```sh
python scripts/documents.py --url 'https://source.example/paper.pdf' --title 'Actual source title' --category candidate-paper
python scripts/import_content.py reviewed-records.json
python scripts/import_content.py reviewed-records.json --apply
python scripts/inventory.py
```

The PDF pipeline retains originals, hashes, text, layout, page renders, embedded images, tables where detected, and uncertain numbered blocks. OCR uses a locally installed `tesseract` when available. Review all mathematics, source identities, diagrams, question numbering and page joins. Automatic numbered blocks are **not verified questions**. Human transcription/reconciliation and marking association are still required. Import rejects duplicate IDs and uncleared published source records.

The owner has confirmed reuse permission. The release bundles 51 correctly attributed complete source-paper PDFs, every source page, and 32 associated source answer guides under `public/source-papers/`. Byte hashes and page counts are checked. These document resources remain separate from the structured scored question bank. Raw acquisition files and extraction drafts stay in the ignored `acquisition/documents/` workspace; source metadata and repeatable scripts are tracked.

## Owner studio

See [administration](docs/ADMINISTRATION.md). The Python server is separate from the student static bundle, uses server-side sessions and CSRF checks, and requires an owner-supplied password. Never put that password in frontend files.

Scanned PDFs require the `tesseract` executable (English language data installed); install Kiswahili language data and adjust OCR language for Kiswahili sources before relying on its transcription. OCR output is never automatically verified. Generate Android PNG icons from the original SVG with `python scripts/icons.py`.

When resuming in a fresh environment, `python scripts/restore_acquisition.py --extract` restores the ignored acquisition workspace from tracked source URLs and verifies each original SHA-256. Use `--id SOURCE_ID` for a single document. Changed or inaccessible sources are reported rather than silently substituted.

## Current book and exam files

The current content release has 122 readable chapters, 3,026 original questions (including 1,009 clearly labelled parameterised numeric drills) and 18 original revision tests. All 36 book manuscripts remain partial. Building exports each manuscript as EPUB and each revision test as a question PDF plus an independently authored answer-guide PDF; downloads appear in Study and Exams and are bundled for offline use. The separate `artifacts/somasmart-original-content-development.zip` contains these original educational files without the application. It contains no redistributed genuine past papers. The application ZIP includes all published learning assets and complete source papers as well. Generated ZIPs are available in the workspace and CI artifacts rather than committed as large Git binaries.

Authored text/exercise batches are kept under `content/batches/`; `content/library.json` is the canonical integrated release. `scripts/regenerate_content.py` deliberately rebuilds from authoring scripts and may replace manual owner edits, so do not use it as an ordinary update command. For new material, upsert reviewed stable IDs or use the validated importer.

The owner has confirmed permission for genuine papers. The first reviewed selection is in Exams → Form Two → Mathematics → Past-paper practice: seven linked Mathematics main questions (18 labelled parts), with source images and independent solutions. Source whole-question marks are retained; self-assessment rubrics are clearly distinguished from official marking. Full manuscript coverage and the remaining paper reviews are still unfinished.

Complete past papers: Exams → choose the form and subject → Past-paper library. Read every page, switch to an associated source answer guide where available, or download the unchanged PDF. The paper notebook saves written working locally. Full-document access does not imply automatic scoring or completed question transcription.

## Interactive source conversion

`python scripts/import_interactive_papers.py` integrates the visually transcribed `content/batches/interactive-*.json` assets. Each source part retains its original number, wording, shared instructions, passages, options and figures; a source-text digest rejects unintended changes. MCQs/matching grade automatically; written answers and drawings require self-marking. Original duplicate option labels and underlining remain visible. The canvas saves diagrams with local attempts.

Paper totals distinguish full transcription from complete scoring. Unresolved source items remain drafts and cannot enter a scored selection. An incorrect source key may have explicitly labelled independently checked guidance; the original question and source guide remain unchanged. `content/interactive-conversion-report.json` and the generated inventory contain actual totals. Source attribution corrections are retained in `content/source-corrections.json`; one archived Chemistry entry was Computer Science with a mismatched guide and is quarantined.

## Build the 180-paper edition

Run `npm run build` followed by `node scripts/verify_release.mjs` and `python scripts/package.py` for the complete offline ZIP with original PDFs. For the size-limited ChatGPT Site, follow the full build with `node scripts/build_hosted.mjs` and `node scripts/verify_release.mjs --hosted`. Package the contents of `dist-hosted/` as the hosted `dist/` directory. This edition includes every archived exam and guide page for offline reading and practice. Opening the linked archive PDF requires internet access.

Run `node scripts/check_offline_papers.mjs dist-hosted` and `node scripts/check_practice_session.mjs dist-hosted` to exercise the built service worker and student application in the test harness.

Each past paper opens its question practice. Choose immediate feedback or marking at submission. Printed question pages preserve the exact source wording and figures. New paper conversions have separate controls for labelled parts and independently authored explanations. Practice points in these conversions use SomaSmart's scoring scale, shown under the paper instructions. Incomplete or ambiguous source items remain answerable as unscored review activities with the problem explained. Written responses use comparison and self-marking.

Run `python scripts/embed_source_practice.py` to import conversion manifests and `python scripts/exam_completion.py --require-complete` to check the individual-response milestone.
