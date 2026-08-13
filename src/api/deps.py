from fastapi import Request

from src.api.state import AppState


def get_state(request: Request) -> AppState:
    """Pull the AppState that app.py attached at startup off the running app."""
    return request.app.state.rag