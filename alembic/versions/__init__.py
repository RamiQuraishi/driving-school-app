"""Alembic migration versions package.

This package contains all database migration versions for the Ontario Driving School Manager.
Each migration file represents a specific change to the database schema.

The migrations are applied in sequence, with each migration depending on the previous one.
This ensures that database changes are applied in the correct order and can be rolled back if needed.
""" 