#!/bin/sh
set -e

if [ -n "${DATABASE_URL:-}" ]; then
    python - <<'PY'
import os
import sys
import time
from urllib.parse import urlparse

import psycopg2

database_url = os.environ["DATABASE_URL"]
parsed = urlparse(database_url)

if parsed.scheme.startswith("postgres"):
    deadline = time.time() + int(os.environ.get("DATABASE_WAIT_TIMEOUT", "60"))
    last_error = None

    while time.time() < deadline:
        try:
            connection = psycopg2.connect(database_url)
            connection.close()
            sys.exit(0)
        except psycopg2.Error as exc:
            last_error = exc
            print("Waiting for PostgreSQL...", flush=True)
            time.sleep(2)

    raise SystemExit(f"PostgreSQL is unavailable: {last_error}")
PY
fi

exec "$@"
