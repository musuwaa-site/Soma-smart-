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

The ZIP is `artifacts/somasmart-development-web.zip`. Serve **all** of `dist/` at the root of an HTTPS static host, with SPA fallback to `index.html`; `sw.js` should use `Cache-Control: no-cache`. Localhost also supports service workers. Do not open `index.html` as a file. `npm run dev` is for development, not offline acceptance. No deployed URL or APK has been produced.

## Installation

Open the HTTPS site on Android Chrome; wait for **Library ready offline**, then use the browser's Install/Add to Home Screen action. Readiness checks every bundled asset, not merely the service-worker registration. If setup fails, free storage and reconnect/reload to retry. Device storage eviction may require reprovisioning. Clearing site data erases progress. Android installation and physical-device behaviour remain unverified.

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

Acquisition originals and rendered third-party content remain in the ignored local `acquisition/documents/` workspace; unresolved copyright material is not pushed to this public repository or bundled into the student app. URL/hash metadata and repeatable acquisition scripts are tracked. Re-running acquisition requires network access. Never infer redistribution permission from a working download.

## Owner studio

See [administration](docs/ADMINISTRATION.md). The Python server is separate from the student static bundle, uses server-side sessions and CSRF checks, and requires an owner-supplied password. Never put that password in frontend files.

Scanned PDFs require the `tesseract` executable (English language data installed); install Kiswahili language data and adjust OCR language for Kiswahili sources before relying on its transcription. OCR output is never automatically verified. Generate Android PNG icons from the original SVG with `python scripts/icons.py`.
