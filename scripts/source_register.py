import pathlib,json
ROOT=pathlib.Path(__file__).resolve().parents[1];metadata=[]
for p in (ROOT/'acquisition/documents').glob('*/source.json'):
 d=json.loads(p.read_text());ex=p.parent/'extraction.json'
 if ex.exists():
  e=json.loads(ex.read_text());d.update(pages=len(e['pages']),draftDetectedBlocks=len(e['questions']),ocrPages=sum(x.get('ocrUsed',False) for x in e['pages']),reviewedQuestionParts=0)
 metadata.append(d)
(ROOT/'acquisition/source-register.json').write_text(json.dumps(metadata,indent=2))
checks=json.loads((ROOT/'acquisition/candidate-checks.json').read_text()) if (ROOT/'acquisition/candidate-checks.json').exists() else []
text='# Source register\n\n'+f'{len(checks)} distinct archive candidate URLs checked with HTTP HEAD; {sum(r["status"]=="reachable" for r in checks)} responded. HTTP reachability is not paper authenticity, content review, curriculum compatibility or reuse clearance. Full candidate metadata is in acquisition/candidate-checks.json.\n\n'
text+='Official TIE source index: https://www.tie.go.tz/publications/syllabus-for-lower-secondary-academics . All nine requested subject syllabuses have been downloaded. Official curriculum source: https://www.tie.go.tz/publications/curriculum-for-lower-secondary-academic . The linked file name references 2026 while the document identifies its citation as 2023; cohort-specific implementation remains unresolved. Historia ya Tanzania na Maadili has its own 2023 syllabus and is not substituted with older History. Official subtopic indexing and language validation are unfinished.\n\n'
text+='NECTA website pages opened. The linked FTNA format returned 404; CIRA 2022/2023 indexes returned 403. No access controls were bypassed. TETEA Form 1–2 archive index was opened and actual document URLs collected; the first downloaded batch is mainly Form Two 2025, including vocational Business/Historia papers whose academic-stream compatibility remains unverified.\n\n'
text+='The owner explicitly confirmed permission to use the examination papers in SomaSmart. This is recorded as owner-attested clearance, not an inspection of an uploaded permission document. Downloaded PDFs and derived page/text/OCR files are retained only in the ignored acquisition workspace. Published genuine-question counts are calculated in content/inventory.json; extraction and marking verification remain separate from owner permission. OCR-detected blocks need manual reconciliation and are not counted as verified answerable parts.\n\n'
for d in sorted(metadata,key=lambda d:d['sourceTitle']):
 text+=f'- **{d["sourceTitle"]}** — {d["category"]}; {d.get("pages",0)} pages; {d.get("draftDetectedBlocks",0)} unverified detected blocks; {d.get("ocrPages",0)} OCR pages. SHA-256 `{d["sha256"]}`. [Source]({d["url"].replace(" ","%20")}).\n'
(ROOT/'docs/SOURCE_REGISTER.md').write_text(text)
print(len(metadata),'source PDFs registered')
