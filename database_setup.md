# Database Setup Guide

## PostgreSQL Installation and Configuration

### 1. Install PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

**macOS (using Homebrew):**
```bash
brew install postgresql
brew services start postgresql
```

**Windows:**
Download and install from: https://www.postgresql.org/download/windows/

### 2. Start PostgreSQL Service

**Ubuntu/Debian:**
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**macOS:**
```bash
brew services start postgresql
```

### 3. Create Database and User

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database
CREATE DATABASE employee_management;

# Create user (optional)
CREATE USER your_username WITH PASSWORD 'your_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE employee_management TO your_username;

# Exit psql
\q
```

### 4. Alternative: Using createdb command

```bash
# Create database directly
createdb -U postgres employee_management
```

### 5. Environment Variables

Create a `.env` file in your project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here

# Database Configuration
DB_NAME=employee_management
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

# Django Settings
ALLOWED_HOSTS=localhost,127.0.0.1
LANGUAGE_CODE=en-us
TIME_ZONE=UTC
```

### 6. Test Connection

```bash
# Test PostgreSQL connection
psql -h localhost -U postgres -d employee_management
```

### 7. Common Issues and Solutions

**Password Authentication Failed:**
- Check if PostgreSQL is running: `sudo systemctl status postgresql`
- Verify password in `.env` file
- Check PostgreSQL authentication configuration in `pg_hba.conf`

**Connection Refused:**
- Ensure PostgreSQL is running
- Check if port 5432 is open
- Verify firewall settings

**Permission Denied:**
- Ensure user has proper privileges
- Check database ownership

### 8. Django Commands

After setting up the database:

```bash
# Activate virtual environment
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### 9. Database Reset (if needed)

```bash
# Drop and recreate database
dropdb -U postgres employee_management
createdb -U postgres employee_management

# Remove migrations and recreate
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Recreate migrations
python manage.py makemigrations
python manage.py migrate
```
