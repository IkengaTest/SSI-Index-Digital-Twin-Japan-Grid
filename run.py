#!/usr/bin/env python3
"""run.py — SSI v4.0 ingestion orchestrator for Japan."""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from config import COUNTRY, MATRIX_PATH, SOURCE_REGISTRY
from common.storage import load_matrix, save_matrix

log = logging.getLogger("ssi.japan")


def run_tier(tier: int) -> None:
    """Execute every source registered for *tier* and persist the matrix."""
    sources = [s for s in SOURCE_REGISTRY if s["tier"] == tier]
    if not sources:
        log.warning("No sources registered for tier %d", tier)
        return

    matrix = load_matrix(MATRIX_PATH)
    for src in sources:
        log.info("Running source: %s (tier %d)", src["name"], tier)
        try:
            df_new = src["fn"]()
            if df_new is not None and not df_new.empty:
                matrix = matrix.combine_first(df_new)
                log.info("  → merged %d rows from %s", len(df_new), src["name"])
        except Exception:
            log.exception("  ✘ %s failed", src["name"])

    save_matrix(matrix, MATRIX_PATH)
    log.info("Tier %d complete — matrix now has %d rows", tier, len(matrix))


def main() -> None:
    parser = argparse.ArgumentParser(description=f"SSI v4.0 — {COUNTRY} ingestion")
    parser.add_argument("--tier", type=int, choices=[1, 2, 3], required=True)
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(name)-24s  %(levelname)-8s  %(message)s",
    )
    log.info("=== SSI %s  |  Tier %d ===" , COUNTRY, args.tier)
    run_tier(args.tier)


if __name__ == "__main__":
    main()
