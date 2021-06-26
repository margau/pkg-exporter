import os
import subprocess

cwd = os.path.join(os.path.dirname(__file__), "..")
cwd = os.path.abspath(cwd)

lint_files = ["texfile.py", "scripts/", "pkgmanager/apt.py"]

subprocess.run(["flake8"] + lint_files, cwd=cwd)
