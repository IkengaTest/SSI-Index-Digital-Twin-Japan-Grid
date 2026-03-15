#!/usr/bin/env python3
"""data_loader.py — HTTP fetch helpers with retry and disk caching."""
from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import Any

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from config import CACHE_DIR, REQUEST_TIMEOUT

log = logging.getLogger(__name__)


def _cache_path(url: str) -> Path:
    """Return a deterministic cache-file path for *url*."""
    digest = hashlib.sha256(url.encode()).hexdigest()[:16]
    return CACHE_DIR / f"{digest}.cache"


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=30))
def fetch_json(url: str, *, params: dict | None = None,
               headers: dict | None = None, use_cache: bool = True) -> Any:
    """GET *url*, return parsed JSON. Results are cached to disk."""
    cache = _cache_path(url + str(params))
    if use_cache and cache.exists():
        log.debug("Cache hit: %s", cache)
        return __import__("json").loads(cache.read_text())

    log.info("Fetching %s", url)
    resp = requests.get(url, params=params, headers=headers,
                        timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    data = resp.json()

    if use_cache:
        cache.write_text(__import__("json").dumps(data))
    return data


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=30))
def fetch_text(url: str, *, params: dict | None = None,
               headers: dict | None = None) -> str:
    """GET *url*, return raw text."""
    log.info("Fetching (text) %s", url)
    resp = requests.get(url, params=params, headers=headers,
                        timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.text


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=30))
def fetch_bytes(url: str, *, params: dict | None = None,
                headers: dict | None = None) -> bytes:
    """GET *url*, return raw bytes (for binary / Parquet files)."""
    log.info("Fetching (bytes) %s", url)
    resp = requests.get(url, params=params, headers=headers,
                        timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.content
