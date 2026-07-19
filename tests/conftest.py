"""Configure sys.path so tests can import the backend app regardless of cwd."""
import sys
from pathlib import Path

backend_path = Path(__file__).resolve().parents[1] / "app" / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))
