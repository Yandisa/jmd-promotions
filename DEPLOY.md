# JMD Promotions — Deployment Guide
### GitHub → Coolify → VPS (51.255.1.140)

---

## Architecture

```
GitHub (code)
    │  git push → main
    ▼
Coolify (on VPS 51.255.1.140)
    ├─ Builds Docker image from Dockerfile
    ├─ Runs entrypoint.sh (migrate → collectstatic → gunicorn)
    ├─ Shared PostgreSQL service (managed by Coolify)
    └─ Persistent volume for /app/media
```

---

## Step 1 — Push to GitHub

```bash
cd jmdsite

git init
git add .
git commit -m "Initial commit — JMD Promotions"

# Create a repo on github.com first, then:
git remote add origin https://github.com/YOUR_USERNAME/jmd-promotions.git
git branch -M main
git push -u origin main
```

---

## Step 2 — Set up Coolify on your VPS

SSH into your VPS and install Coolify:

```bash
ssh root@51.255.1.140

curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash
```

Then open **http://51.255.1.140:8000** in your browser and complete the Coolify setup wizard.

---

## Step 3 — Create PostgreSQL in Coolify

1. Coolify sidebar → **Resources** → **+ New Resource**
2. Choose **PostgreSQL**
3. Set:
   - **Name:** `jmd-postgres`
   - **Database:** `jmd_db`
   - **Username:** `jmd_user`
   - **Password:** (generate a strong one and save it)
4. Click **Deploy**
5. Once running, click on the service → **Connection** tab
6. Note the **internal host** (e.g. `postgresql.coolify.internal` or the container name)

---

## Step 4 — Create the Django App in Coolify

1. Coolify → **+ New Resource** → **Application**
2. Choose **Docker** → **From a GitHub Repository**
3. Connect your GitHub account and select `jmd-promotions` repo
4. Branch: `main`
5. **Build Pack:** Dockerfile (auto-detected)
6. **Port:** `8000`

### Environment Variables (paste these in Coolify → Environment)

```env
SECRET_KEY=generate-a-50-char-random-string-here
DEBUG=False
ALLOWED_HOSTS=51.255.1.140,yourdomain.co.za
CSRF_TRUSTED_ORIGINS=http://51.255.1.140,https://51.255.1.140,https://yourdomain.co.za

# PostgreSQL — from Step 3
DB_NAME=jmd_db
DB_USER=jmd_user
DB_PASSWORD=your-postgres-password-from-step-3
DB_HOST=jmd-postgres          # Coolify internal service name
DB_PORT=5432

# Admin user — created automatically on first deploy
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=choose-a-strong-password
DJANGO_SUPERUSER_EMAIL=admin@jmdpromotions.co.za

# Gunicorn
GUNICORN_WORKERS=3
GUNICORN_TIMEOUT=120
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### Persistent Volume (for uploaded images)

In Coolify → your app → **Storage**:
- Source: `jmd_media` (Coolify manages this)
- Destination: `/app/media`

---

## Step 5 — Deploy

Click **Deploy** in Coolify. Watch the logs:

```
✅ PostgreSQL is ready
🔄 Running migrations...
📦 Collecting static files...
👤 Creating/updating superuser: admin
🌱 Demo data loaded.
🚀 Starting Gunicorn
```

Your site is live at **http://51.255.1.140**

---

## Step 6 — Auto-deploy on git push (optional)

1. In Coolify → your app → **Settings** → **Webhooks**
2. Copy the **Deploy Webhook URL**
3. In GitHub → your repo → **Settings** → **Secrets and variables** → **Actions**
4. Add secret: `COOLIFY_WEBHOOK_URL` = (the URL from Coolify)

Now every `git push` to `main` triggers an automatic deploy.

---

## Updating the site

```bash
# Make your changes locally
git add .
git commit -m "Your change description"
git push origin main
# Coolify auto-deploys within ~60 seconds
```

---

## Useful Coolify tips

| Task | How |
|------|-----|
| View live logs | App → Logs tab |
| Restart app | App → Actions → Restart |
| Run Django command | App → Terminal → `python manage.py <command>` |
| Change env vars | App → Environment → redeploy after saving |
| Database backups | PostgreSQL service → Backups tab |

---

## Local development (Docker Compose)

```bash
cp .env.example .env
# Edit .env — set DB_PASSWORD etc.

docker compose up --build
# Visit http://localhost:8000
# Admin: http://localhost:8000/admin  →  admin / (your DJANGO_SUPERUSER_PASSWORD)
```

---

## Troubleshooting

**500 error on first load**
- Check Coolify logs for migration errors
- Verify DB_HOST matches the PostgreSQL service name exactly

**Static files not loading**
- Whitenoise handles static files — no separate nginx needed
- Make sure `collectstatic` ran in the entrypoint logs

**Can't connect to PostgreSQL**
- In Coolify, both services must be in the **same network**
- Check the PostgreSQL service name matches DB_HOST

**Media files missing after redeploy**
- Ensure the `/app/media` volume is configured in Coolify Storage
- Volumes persist across deploys automatically

---

## Domain setup (when you have one)

1. Point your domain's A record to `51.255.1.140`
2. In Coolify → your app → **Domains** → add `yourdomain.co.za`
3. Enable **Let's Encrypt** for free SSL
4. Update env vars:
   ```
   ALLOWED_HOSTS=51.255.1.140,yourdomain.co.za
   CSRF_TRUSTED_ORIGINS=https://yourdomain.co.za
   ```
5. Redeploy
