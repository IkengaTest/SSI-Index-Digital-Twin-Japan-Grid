#!/usr/bin/env python3
"""publish.py — Push latest matrix to the SSI dashboard repo via PyGithub."""
from __future__ import annotations

import logging
import sys
from base64 import b64encode
from pathlib import Path

from github import Github, GithubException

from config import COUNTRY, COUNTRY_CODE, DASHBOARD_TOKEN, MATRIX_PATH

log = logging.getLogger("ssi.japan.publish")

DASHBOARD_REPO = "ikengassiindex/ikengassiindex.github.io"
DASHBOARD_PATH = f"{COUNTRY_CODE.lower()}/matrix_{COUNTRY.lower()}.parquet"
BRANCH = "main"


def publish() -> None:
    """Upload the local matrix parquet to the dashboard repo."""
    if not DASHBOARD_TOKEN:
        log.error("DASHBOARD_TOKEN not set — aborting publish")
        sys.exit(1)

    matrix = Path(MATRIX_PATH)
    if not matrix.exists():
        log.error("Matrix file not found at %s", matrix)
        sys.exit(1)

    gh = Github(DASHBOARD_TOKEN)
    repo = gh.get_repo(DASHBOARD_REPO)
    content_bytes = matrix.read_bytes()
    message = f"chore({COUNTRY_CODE}): update matrix — {COUNTRY} Digital-Twin"

    try:
        existing = repo.get_contents(DASHBOARD_PATH, ref=BRANCH)
        repo.update_file(
            path=DASHBOARD_PATH,
            message=message,
            content=content_bytes,
            sha=existing.sha,
            branch=BRANCH,
        )
        log.info("Updated %s in %s", DASHBOARD_PATH, DASHBOARD_REPO)
    except GithubException as exc:
        if exc.status == 404:
            repo.create_file(
                path=DASHBOARD_PATH,
                message=message,
                content=content_bytes,
                branch=BRANCH,
            )
            log.info("Created %s in %s", DASHBOARD_PATH, DASHBOARD_REPO)
        else:
            raise


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(name)-24s  %(levelname)-8s  %(message)s",
    )
    publish()
