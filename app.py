import os
import sys
import importlib.util

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUBDIR = os.path.join(BASE_DIR, '5.Project Development Phase')
SUBAPP_PATH = os.path.join(SUBDIR, 'app.py')

# Ensure the subdirectory is on sys.path for submodule imports like src.predict
if SUBDIR not in sys.path:
    sys.path.insert(0, SUBDIR)

spec = importlib.util.spec_from_file_location('backend_app', SUBAPP_PATH)
backend_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backend_app)

app = backend_app.app
