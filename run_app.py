"""Launch the Urban Survey Report Generator GUI."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Force Python UTF-8 mode on Windows
os.environ["PYTHONUTF8"] = "1"

# Fix Windows console encoding for Arabic output
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Ensure project root is on the path
sys.path.insert(0, str(Path(__file__).parent))
load_dotenv()

from src.gui import main

if __name__ == "__main__":
    main()
