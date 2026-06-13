# Testing

Tests are organized by scope:

```text
tests/
├── unit/
├── integration/
├── factories/
└── conftest.py
```

Run the suite with:

```bash
pytest
```

Run quality checks with:

```bash
ruff check .
black --check .
isort --check-only .
```

Current coverage focuses on authentication, public pages, models, forms, contact submission, admin access protection, and API read/contact flows.
