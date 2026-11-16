import pathlib,shutil
root=pathlib.Path(__file__).resolve().parents[1]

import subprocess,sys
subprocess.run(['node',str(root/'scripts/student-release.mjs'),str(root/'public/library.json')],cwd=root,check=True)
subprocess.run([sys.executable,str(root/"scripts/export_books.py")],check=True)

subprocess.run([sys.executable,str(root/"scripts/export_exams.py")],check=True)
