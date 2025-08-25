#!/usr/bin/env bash
set -e

# Wait for DB if using a remote Postgres
if [ -n "$DB_HOST" ]; then
  echo "Waiting for database $DB_HOST:$DB_PORT..."
  until python - <<PY
import os, psycopg2, time
host=os.getenv('DB_HOST','localhost')
port=os.getenv('DB_PORT','5432')
user=os.getenv('DB_USER','postgres')
password=os.getenv('DB_PASSWORD','postgres')
db=os.getenv('DB_NAME','employee_management')
try:
    psycopg2.connect(host=host, port=port, user=user, password=password, dbname=db)
    print('DB is up')
except Exception as e:
    print('DB not ready:', e)
    raise SystemExit(1)
PY
  do
    sleep 1
  done
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput || true

# Start server
exec gunicorn employee_project.wsgi:application --bind 0.0.0.0:8000 --workers 3
