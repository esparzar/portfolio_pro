"""Backward-compatible API registration module.

New applications should import `register_api` from `app.api`.
"""

from app.api import register_api

__all__ = ["register_api"]
