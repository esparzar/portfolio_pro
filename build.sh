#!/usr/bin/env bash
# Render / CI: avoid PyPI package "jwt" shadowing PyJWT (breaks flask-jwt-extended:
# ImportError: cannot import name 'Options' from 'jwt.types')
set -euo pipefail
pip uninstall -y jwt 2>/dev/null || true
pip install --no-cache-dir -r requirements.txt
