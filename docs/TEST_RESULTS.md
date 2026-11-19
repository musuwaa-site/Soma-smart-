# Test evidence — release 0.6.0

64 automated tests passed: 40 Node and 24 Python. The final source bank includes 299 genuine scored records from 14 paper sources ; 13 new complete transcriptions preserve 446 editorial records, including 154 held items. Production-format build passed; all 689 offline assets passed hash/inclusion checks.

New source-conversion tests verify exact canonical-versus-batch text digests (wording, labels, options, passages, underlining, tables), reject accidental source wording edits, and check original PDF hashes/full-page references. The mismatched ComputerScience/Chemistry archive association is quarantined. Student JSON and the offline asset set exclude unpublished question drafts/quarantined source associations.

Actual genuine banks are checked against eligible published selections. Tests cover full source totals, fractional source marks, objective/matching keys, pending written self-marking, whole shared-material groups, seeded selection, repeated original option labels and underlined source words. Full 100-mark Mathematics/Business/Historia papers reach100 only after required written self-assessment. Independent guide corrections do not alter source questions.

Existing owner HTTP authorization/CSRF tests, PDF extraction, EPUB/XML/PDF exports, deterministic exports, all 18 subject/form combinations, saved-result calculations and service-worker simulations pass. Simulated worker tests cover successful provisioning, quota/interruption/corruption failure and preservation of the previous complete release. These are not real-browser acceptance.

Not performed: real-browser drawing/pointer interaction, IndexedDB persistence/upgrade, offline Android installation and complete unseen-content workflow, real-browser interrupted updates/storage eviction. No CUA browser tool is mounted; no browser was installed or improvised. Canvas code passes JS parsing/build but is not described as browser-tested.

The overall readiness gate remains failed for incomplete books/curriculum, genuine-bank targets and missing browser/Android/migration acceptance. Current test and build evidence validates this populated development milestone, not production completeness.

Startup/access repair: six new tests cover Unicode streaming/progress, authentication responses, HTML sign-in responses, stalled network requests, unreachable/malformed data and storage timeouts without data deletion. Production DNS and authenticated critical-asset HTTP checks succeeded; these do not reproduce the user’s browser connection error. See ACCESS_DIAGNOSIS.md.

Release 0.7.0 passed 66 automated tests. New checks cover alternate objective keys and preservation of the original parts under source-verified whole-question marks. The offline build includes 641 scored genuine records. The guided exam review remains unverified on a physical Android device.

Release 0.8.0 passed 67 automated tests. The source practice test checks coverage of the 29 added papers, 282 selectable groups, printed order, unclipped source-page references and exclusion from the scored question bank. Browser and device acceptance remain pending.

Release 0.9.0 passes 68 automated tests, including exact paper binding and the 100-mark total for the independent guide. The offline package was built and checked.

Release 0.10.0 checks the original scan reading order and both independent guide totals. The combined suite has 69 automated tests.

Release 0.11.0 checks all 67 self-check selections and the source bindings for two full Mathematics guides and one partial Physics guide.

## Release 0.12.0

All 45 Node and 24 Python tests passed. The full ZIP build verified 1,462 offline assets (305.9 MiB expanded) and the private Site build verified 1,305 (83.2 MiB expanded). Both contained 125 interactive papers. The full build preserved every archive PDF hash. The hosted build preserved every published paper and guide page.

With the network disabled after installation in the service-worker harness, both builds served the library and every selected question page across 1,012 groups. The application harness selected questions, entered answers, saved review status, and restarted the app for all 103 page-based papers. For questions with a guide it also checked saved self-marks. The 22 other papers passed scored-record and marking checks. These runs used JavaScript test doubles for device storage and browser APIs. Visual browser and physical Android acceptance are still open.

## Release 0.13.0

45 Node tests and 24 Python tests passed. Both builds verified 180 distinct papers. The full release validated 1,909 assets and the hosted release validated 1,697. After simulated network disconnection, both service workers served the published library and the original pages for every one of 1,615 question groups. All 158 page-based selections restored typed answers and review status on restart in the application harness. The scored-bank tests exercised automatic marking and written self-assessment, including both newly converted 100-mark papers. A second import produced an identical canonical library SHA-256. Physical Android testing remains pending.

The manual offline download update passed 46 Node tests and 24 Python tests. Worker tests cover zero download requests on installation, explicit start, abort on pause, resumption, offline fallback and cache validation.
The student navigation harness verified leaving a scored exam for the dashboard and reopening its saved answer. The hosted and full offline packages passed integrity checks.

Release 0.14.0 passed 47 Node tests and 24 Python tests. The built application harness opened old paper links into practice, checked a correct immediate response, withheld feedback for an incorrect end-mode response until submission, and verified saved answers after reopening. Both packages passed integrity validation. Offline worker checks exercised all 180 papers. All 676 published genuine scored records have an offline student-facing explanation.
