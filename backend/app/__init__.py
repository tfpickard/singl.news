from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from the project root .env file so modules that
# access os.environ at import time (e.g. narrative.py) see the configured values.
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env", override=False)
