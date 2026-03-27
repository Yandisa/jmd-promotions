# ── Stage 1: Builder ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt


# ── Stage 2: Runtime ─────────────────────────────────────────────────────────
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local

# Create non-root user with a real home directory
# python:3.12-slim uses Debian's adduser — no --create-home flag needed,
# home is created by default when --home is specified without --no-create-home
RUN addgroup --system jmd && \
    adduser --system --ingroup jmd --home /home/jmd jmd

WORKDIR /app

COPY --chown=jmd:jmd . .

RUN mkdir -p /app/static /app/media /app/staticfiles && \
    chown -R jmd:jmd /app/static /app/media /app/staticfiles

RUN chmod +x entrypoint.sh

USER jmd

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
