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
