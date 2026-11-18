import subprocess,sys
for script in ['seed_content.py','enrich.py','batch_two.py','batch_form_two.py','workbook_batch.py','revision_papers.py','expansion_diagrams.py','embed_curriculum.py','verify_first_paper.py','legacy_revision_exercises.py','batch_form_one.py','calculation_drills.py','import_chapter_assets.py','additional_calculation_drills.py','preserve_question_context.py','revision_papers.py','bundle_source_papers.py','import_interactive_papers.py','embed_source_practice.py','prepare_dev.py','inventory.py']:
 subprocess.run([sys.executable,'scripts/'+script],check=True)
