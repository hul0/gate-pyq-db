"""
studiva_ocr - Intelligent, rate-limited, multi-threaded OCR and dataset builder for GATE question papers.
"""

import sys
import os
import glob

# Ensure workspace .venv site-packages is in sys.path if running under system python
if "cv2" not in sys.modules:
    venv_site = glob.glob(os.path.join(os.getcwd(), ".venv", "lib", "python*", "site-packages"))
    for p in venv_site:
        if p not in sys.path:
            sys.path.insert(0, p)

__version__ = "1.0.0"
