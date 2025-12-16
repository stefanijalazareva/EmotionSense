# PostgreSQL Setup Guide for EmotionSense

## Prerequisites
- PostgreSQL 13+ installed on your system
- PostgreSQL server running

## Database Configuration

We use **two separate databases**:
- `emotionsense_dev` - Development/testing database
- `emotionsense_prod` - Production database

## Setup Steps

### 1. Install PostgreSQL (if not installed)
Download from: https://www.postgresql.org/download/windows/

### 2. Start PostgreSQL Service
```powershell
# Check if PostgreSQL is running
Get-Service -Name postgresql*

# Start if not running
Start-Service postgresql-x64-15  # Adjust version number
```

### 3. Create Databases

**Option A: Using psql (Command Line)**
```bash
# Connect to PostgreSQL
psql -U postgres

# Run the setup script
\i docs/setup_databases.sql

# Or create manually:
CREATE DATABASE emotionsense_dev;
CREATE DATABASE emotionsense_prod;

# Exit
\q
```

**Option B: Using pgAdmin (GUI)**
1. Open pgAdmin
2. Connect to PostgreSQL server
3. Right-click "Databases" → Create → Database
4. Create `emotionsense_dev`
5. Repeat for `emotionsense_prod`

**Option C: Using PowerShell**
```powershell
# Run SQL file directly
$env:PGPASSWORD="your-password"; psql -U postgres -f docs/setup_databases.sql
```

### 4. Configure Environment

Edit `backend/.env`:
```env
ENVIRONMENT=dev              # Use 'dev' for development, 'prod' for production
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Run Migrations

**For Development:**
```bash
cd backend
# Ensure ENVIRONMENT=dev in .env
python manage.py migrate
```

**For Production:**
```bash
cd backend
# Change ENVIRONMENT=prod in .env
python manage.py migrate
```

## Switching Between Databases

Simply change the `ENVIRONMENT` variable in your `.env` file:
- `ENVIRONMENT=dev` → Uses `emotionsense_dev`
- `ENVIRONMENT=prod` → Uses `emotionsense_prod`

## Verify Connection

```bash
cd backend
python manage.py dbshell
```

You should see:
```
psql (15.x)
Type "help" for help.

emotionsense_dev=>
```

## Common Issues

### Issue: "psycopg2" ImportError
```bash
pip install psycopg2-binary
```

### Issue: Password authentication failed
1. Edit `pg_hba.conf` (usually in PostgreSQL installation directory)
2. Change `md5` to `trust` for local connections (development only)
3. Restart PostgreSQL service

### Issue: Port 5432 in use
Check if another service is using the port:
```powershell
netstat -ano | findstr :5432
```

## Backup Commands

**Backup Dev Database:**
```bash
pg_dump -U postgres emotionsense_dev > backup_dev.sql
```

**Restore Dev Database:**
```bash
psql -U postgres emotionsense_dev < backup_dev.sql
```

**Copy Dev to Prod (when ready):**
```bash
# Backup dev
pg_dump -U postgres emotionsense_dev > migrate_to_prod.sql

# Restore to prod
psql -U postgres emotionsense_prod < migrate_to_prod.sql
```

## Database Management

**View all databases:**
```sql
\l
```

**Connect to specific database:**
```sql
\c emotionsense_dev
```

**View tables:**
```sql
\dt
```

**Drop database (careful!):**
```sql
DROP DATABASE emotionsense_dev;
```
