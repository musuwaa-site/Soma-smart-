# Owner administration

Set a unique password of at least 16 characters in `SOMASMART_ADMIN_PASSWORD`, then run `python admin/server.py`. It binds only to localhost at port 8765. There is no default password. For remote Android access, deploy behind an authenticated HTTPS reverse proxy and set `SOMASMART_ADMIN_SECURE=1` so session cookies require HTTPS. Do not expose the plain HTTP server directly to the internet. The initial server uses one environment-configured owner credential and in-memory expiring sessions; it is not a managed multi-user service.

Sign in; choose lessons/questions/glossary/papers/books; edit structured records; apply edits; save draft. Source metadata is shown for review. Import accepts a structured complete release into the owner draft. The editor is touch usable but raw JSON; specialised diagram upload and PDF review tooling remain unfinished. Media paths must point to existing local `public/` assets.

Publishing validates source data and atomically replaces `content/library.json`. It does not bypass the final release gate or deploy software. Run tests, build, verify the bundle and review the inventory before distributing. Edits to drafts do not change published student data.

States are draft → verified → published. Third-party scored items require a registered real paper, source reference, cleared/open/public-domain rights, verified extraction, valid marks and a marking resource. Independent solutions must be labeled as such. Source PDF review happens in the acquisition workspace; originals do not belong in the public student bundle without clearance.

For Kiswahili OCR use installed language data and `--ocr-language swa` (or `eng+swa` for mixed text) with `scripts/documents.py`. The initial acquisition used English OCR and remains unverified. Never publish its transcription without comparing the original rendered page.
