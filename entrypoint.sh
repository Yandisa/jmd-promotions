#!/bin/sh
set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  JMD Promotions — Starting up"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done
echo "✅ PostgreSQL is ready"

# Run migrations
echo "🔄 Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if DJANGO_SUPERUSER_* env vars are set
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "👤 Creating/updating superuser: $DJANGO_SUPERUSER_USERNAME"
  python manage.py shell -c "
from django.contrib.auth.models import User
u, created = User.objects.get_or_create(username='$DJANGO_SUPERUSER_USERNAME')
u.set_password('$DJANGO_SUPERUSER_PASSWORD')
u.is_staff = True
u.is_superuser = True
u.email = '${DJANGO_SUPERUSER_EMAIL:-admin@jmdpromotions.co.za}'
u.save()
print('  Created!' if created else '  Already exists — password updated.')
"
fi

# Load initial demo data if DB is empty (first deploy only)
echo "🌱 Checking demo data..."
python manage.py shell -c "
from core.models import OrderStep
from store.models import Category
if not Category.objects.exists():
    import subprocess
    subprocess.run(['python', 'manage.py', 'setup_demo'], check=True)
    print('  Demo data loaded.')
else:
    print('  Data already exists — skipping.')
"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Starting Gunicorn"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

exec gunicorn jmd.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers "${GUNICORN_WORKERS:-3}" \
    --timeout "${GUNICORN_TIMEOUT:-120}" \
    --access-logfile - \
    --error-logfile - \
    --log-level info
