import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src')
SETTINGS = os.path.join(ROOT, 'settings')

for path in (SRC, SETTINGS):
    if path not in sys.path:
        sys.path.insert(0, path)