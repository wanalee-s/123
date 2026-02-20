#!/bin/bash
# Scripts to run AuthUser migration from Supabase to local database

set -e

CONTAINER_NAME="${1:-roomsync_fastapi_1}"

echo "🔄 Migrating AuthUser data..."
echo "Container: $CONTAINER_NAME"
echo ""

# Check if container exists
if ! docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "❌ Container '$CONTAINER_NAME' not found"
    echo ""
    echo "Available containers:"
    docker ps -a --format '{{.Names}}' | grep fastapi || echo "  (No FastAPI containers found)"
    exit 1
fi

# Run migration
docker exec -it "$CONTAINER_NAME" python /app/migrate_authusers.py

echo ""
echo "Done! Check migration results above."
