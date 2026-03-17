#!/usr/bin/env bash
set -euo pipefail

DUMP_FILE="${1:-}"

if [[ -z "$DUMP_FILE" ]]; then
    echo "Usage: $0 <path-to-db-dump>" >&2
    exit 1
fi

if [[ ! -f "$DUMP_FILE" ]]; then
    echo "Error: dump file '$DUMP_FILE' not found" >&2
    exit 1
fi

: "${POSTGRES_USER:=ausgsteckt}"
: "${POSTGRES_PASSWORD:=ausgsteckt}"
export POSTGRES_USER POSTGRES_PASSWORD

cleanup() {
    echo "Stopping containers..."
    podman-compose down 2>/dev/null || true
}
trap cleanup EXIT INT TERM

# Tear down any existing containers to start clean
podman-compose down 2>/dev/null || true

# Rebuild images to pick up any changes
podman-compose build

# Start db first
echo "Starting database..."
podman-compose up -d db

# Wait for postgres to be ready
echo "Waiting for database to be ready..."
DB_CONTAINER=$(podman ps --filter "label=com.docker.compose.service=db" --format "{{.Names}}" | head -1)
# The postgis image init sequence logs "ready to accept connections" twice:
# once during init (runs init scripts, installs PostGIS), then shuts down and
# restarts in normal mode. Wait for the second occurrence to avoid loading the
# dump while postgres is mid-restart.
until [ "$(podman logs "$DB_CONTAINER" 2>&1 | grep -c 'ready to accept connections')" -ge 2 ]; do
    sleep 1
done

# Load the dump — detect format by magic bytes, not filename
echo "Loading dump: $DUMP_FILE"
case "$DUMP_FILE" in
    *.xz)  DECOMPRESS="xz -dc" ;;
    *.zst) DECOMPRESS="zstd -dc" ;;
    *)     DECOMPRESS="" ;;
esac

if [[ -n "$DECOMPRESS" ]]; then
    MAGIC=$(set +o pipefail; $DECOMPRESS "$DUMP_FILE" | head -c 5)
else
    MAGIC=$(head -c 5 "$DUMP_FILE")
fi

if [[ "$MAGIC" == "PGDMP" ]]; then
    if [[ -n "$DECOMPRESS" ]]; then
        $DECOMPRESS "$DUMP_FILE" | podman exec -i "$DB_CONTAINER" pg_restore -U "$POSTGRES_USER" -d ausgsteckt --clean --if-exists
    else
        podman cp "$DUMP_FILE" "$DB_CONTAINER:/tmp/db_dump"
        podman exec "$DB_CONTAINER" pg_restore -U "$POSTGRES_USER" -d ausgsteckt --clean --if-exists /tmp/db_dump
    fi
else
    if [[ -n "$DECOMPRESS" ]]; then
        $DECOMPRESS "$DUMP_FILE" | podman exec -i "$DB_CONTAINER" psql -U "$POSTGRES_USER" -d ausgsteckt
    else
        podman cp "$DUMP_FILE" "$DB_CONTAINER:/tmp/db_dump"
        podman exec "$DB_CONTAINER" psql -U "$POSTGRES_USER" -d ausgsteckt -f /tmp/db_dump
    fi
fi
echo "Dump loaded."

# Start everything and follow logs
podman-compose up --no-recreate
