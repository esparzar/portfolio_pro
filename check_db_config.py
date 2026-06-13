#!/usr/bin/env python
"""Check database configuration for local and Render environments."""

import os
import sys

from dotenv import load_dotenv

load_dotenv()


def check_database_config():
    """Check whether DATABASE_URL is configured for persistent storage."""
    print("\n" + "=" * 60)
    print("DATABASE CONFIGURATION CHECKER")
    print("=" * 60 + "\n")

    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        print("DATABASE_URL not found in environment variables.")
        print("Issue: the app will use local SQLite fallback storage.")
        print("Solution: set DATABASE_URL to a PostgreSQL connection URL on Render.\n")
        return False

    print("DATABASE_URL is set.\n")

    if database_url.startswith(("postgresql://", "postgres://")):
        print("Database Type: PostgreSQL")
        print("Status: production-ready persistent storage\n")
        parts = database_url.split("@", maxsplit=1)
        if len(parts) > 1:
            host_part = parts[1].split("/", maxsplit=1)[0]
            db_name = database_url.rsplit("/", maxsplit=1)[-1]
            print(f"Database Host: {host_part}")
            print(f"Database Name: {db_name}\n")
        return True

    if "sqlite" in database_url:
        print("Database Type: SQLite")
        print("Status: ephemeral for Render deployments\n")
        return False

    print("Unknown database type. Verify DATABASE_URL before deploying.\n")
    return False


if __name__ == "__main__":
    success = check_database_config()

    print("=" * 60)
    if success:
        print("Database configuration looks good.")
        sys.exit(0)

    print("Database needs to be configured. See instructions above.")
    sys.exit(1)
