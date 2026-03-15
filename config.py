#!/usr/bin/env python3
"""config.py — Central configuration for SSI Japan Digital-Twin."""
from __future__ import annotations

import os
from pathlib import Path

# ---- Country identity ----
COUNTRY = "Japan"
COUNTRY_CODE = "JP"
TIMEZONE = "Europe/Zurich"

# ---- Paths ----
BASE_DIR = Path(__file__).resolve().parent
MATRIX_PATH = BASE_DIR / "matrix_japan.parquet"
CACHE_DIR = BASE_DIR / ".cache"
CACHE_DIR.mkdir(exist_ok=True)

# ---- API credentials (injected via GitHub Actions secrets) ----
CDS_API_KEY = os.getenv("CDS_API_KEY", "")
ENTSOE_TOKEN = os.getenv("ENTSOE_TOKEN", "")
DASHBOARD_TOKEN = os.getenv("DASHBOARD_TOKEN", "")

# ---- Networking ----
REQUEST_TIMEOUT = 120  # seconds

# ---- Source registry (populated by @register_source) ----
SOURCE_REGISTRY: list[dict] = []


def register_source(tier: int):
    """Decorator: register a callable as a data source for *tier*."""
    def decorator(fn):
        SOURCE_REGISTRY.append({"name": fn.__name__, "tier": tier, "fn": fn})
        return fn
    return decorator
