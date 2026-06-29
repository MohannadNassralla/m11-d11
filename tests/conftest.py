"""Autograder conftest. Resolves imports from the repo root.

`app.py` lives at the repo root (one level above this `tests/` folder),
so we add the parent directory to sys.path before any tests import it.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
