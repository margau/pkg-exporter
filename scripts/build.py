#!/usr/bin/env python3

import os
import subprocess

cwd = os.path.join(os.path.dirname(__file__), "..")
cwd = os.path.abspath(cwd)

subprocess.run(["pyinstaller", "--onefile", "-n", "pkg_exporter", "src/pkg_exporter/textfile.py"], cwd=cwd)
