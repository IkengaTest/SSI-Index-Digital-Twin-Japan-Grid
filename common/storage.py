#!/usr/bin/env python3
"""storage.py — Parquet-backed matrix helpers for SSI Japan."""
from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

log = logging.getLogger(__name__)


def load_matrix(path: str | Path) -> pd.DataFrame:
    """Load the scoring matrix from *path*, or return an empty frame."""
    path = Path(path)
    if path.exists():
        df = pd.read_parquet(path)
        log.info("Loaded matrix from %s  (%d rows)", path, len(df))
        return df
    log.warning("Matrix not found at %s — starting empty", path)
    return pd.DataFrame()


def save_matrix(df: pd.DataFrame, path: str | Path) -> None:
    """Persist *df* as a Parquet file at *path*."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=True)
    log.info("Saved matrix → %s  (%d rows)", path, len(df))
