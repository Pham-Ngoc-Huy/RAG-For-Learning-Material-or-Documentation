# Vercel Python entrypoint: expose the FastAPI ASGI `app` from the project
# Ensures project root is on PYTHONPATH so `src` can be imported
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.api.app import app  # noqa: E402,F401
