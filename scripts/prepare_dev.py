import pathlib,shutil
root=pathlib.Path(__file__).resolve().parents[1];shutil.copyfile(root/'content/library.json',root/'public/library.json')

import subprocess,sys
subprocess.run([sys.executable,str(root/"scripts/export_books.py")],check=True)

subprocess.run([sys.executable,str(root/"scripts/export_exams.py")],check=True)
