# GuardianAI Alembic Migration Guide & Workflow

This directory manages database schema migrations for GuardianAI using **Alembic** and **SQLAlchemy 2.0**.

---

## 1. Environment & Model Discovery

Alembic reads database connection settings dynamically from Pydantic Settings (`settings.DATABASE_URL`) in [`alembic/env.py`](file:///c:/Users/rajbh/OneDrive/Desktop/GuardianAI/backend/alembic/env.py).

All SQLAlchemy ORM models (`app/models/user.py`, `app/models/scan.py`) register with `Base.metadata` in `env.py` to enable auto-generation of revision scripts.

---

## 2. Common Alembic Migration Commands

### Applying Migrations
```bash
# From the backend directory with venv activated:

# Apply all pending migrations to the latest revision (head)
alembic upgrade head

# Apply a specific revision ID
alembic upgrade 0001_initial_schema
```

### Generating New Migrations
```bash
# Auto-generate a migration revision script after modifying SQLAlchemy ORM models
alembic revision --autogenerate -m "Add email_verified_at column to users table"
```

### Rolling Back Migrations
```bash
# Rollback the last applied migration step
alembic downgrade -1

# Rollback to initial state (base)
alembic downgrade base
```

### Inspecting History & Status
```bash
# Display currently applied migration revision
alembic current

# Display migration revision history graph
alembic history --verbose
```

---

## 3. Database Migration Best Practices

1. **Review Auto-Generated Scripts:** Always inspect auto-generated revision scripts in `alembic/versions/` before running `alembic upgrade head`. Verify table names, index names, and foreign keys.
2. **Reversible Migrations:** Ensure every `upgrade()` function has a matching, non-destructive `downgrade()` function.
3. **Data Loss Safety:** Avoid dropping columns or tables directly in production without a multi-phase deprecation window.
4. **Index Naming Conventions:** Use explicit index naming patterns (`ix_<table_name>_<column_name>`) for query optimization.
