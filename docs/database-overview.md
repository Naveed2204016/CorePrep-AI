# Database Overview

## Database technology
The project documentation identifies MySQL as the relational database and SQLAlchemy as the ORM layer. PyMySQL is used for MySQL connectivity.

## Configuration
The backend database connection is configured through the `DATABASE_URL` environment variable. The README gives this illustrative format:

```text
mysql+pymysql://YOUR_USER:YOUR_PASSWORD@localhost:3306/coreprep_ai
```

Replace the placeholders with local credentials. Never commit a real connection string.

## Documented application data
The README describes persistent information associated with:
- User accounts and profiles
- Learning roadmaps and roadmap topics
- Learning resources
- Assessments and examination results
- Company-preparation activity

This is a conceptual overview, not a verified table-by-table schema. Consult the current SQLAlchemy models and database initialization code for exact table names, columns, relationships, and constraints.

## Local database setup
Create a database using a MySQL client:

```sql
CREATE DATABASE coreprep_ai
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Then set `DATABASE_URL` in `backend/.env`.

## Safe database practices
- Keep production and development databases separate.
- Never commit credentials or real user data.
- Back up important data before applying schema changes.
- Test database changes against a development database first.
