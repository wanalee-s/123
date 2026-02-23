#!/usr/bin/env python3
"""
Migrate AuthUser records from Supabase to local database
Can be run manually or triggered via CLI
Usage: python migrate_authusers.py
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from roomsync.fastapi.app.routers import rooms
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.models.authuser import AuthUser
from app.models.room import Room
from app.db import Base

# Load environment
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    load_dotenv(env_file)

# Get credentials from environment
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")
LOCAL_DB_URL = os.getenv("DATABASE_URL", "postgresql://hello_flask:hello_flask@db:5432/hello_flask_dev")

if not SUPABASE_DB_URL:
    print("❌ Error: SUPABASE_DB_URL not set in .env")
    sys.exit(1)

print(f"📦 Source (Supabase): {SUPABASE_DB_URL[:40]}...")
print(f"📦 Destination (Local): {LOCAL_DB_URL[:40]}...")
print()

# Create engines with retry logic
try:
    supabase_engine = create_engine(SUPABASE_DB_URL, pool_pre_ping=True, connect_args={"timeout": 10})
    local_engine = create_engine(LOCAL_DB_URL, pool_pre_ping=True, connect_args={"timeout": 10})
except Exception as e:
    print(f"❌ Failed to create database engines: {e}")
    sys.exit(1)

# Create session factories
SupabaseSession = sessionmaker(bind=supabase_engine)
LocalSession = sessionmaker(bind=local_engine)

# Ensure local tables exist
try:
    Base.metadata.create_all(local_engine)
    print("✓ Local database tables ready")
except Exception as e:
    print(f"❌ Error creating local tables: {e}")
    sys.exit(1)

# Migrate data
try:
    supabase_db = SupabaseSession()
    local_db = LocalSession()
    
    # Get all Data records from Supabase
    supabase_users = supabase_db.query(AuthUser).all()
    supabase_rooms = supabase_db.query(Room).all()

    print(f"Found {len(supabase_users)} users in Supabase\n")
    print(f"Found {len(supabase_rooms)} rooms in Supabase\n")
    
    if len(supabase_users) == 0 and len(supabase_rooms) == 0:
        print("✅ No data to migrate")
        sys.exit(0)
    
    # Get existing emails in local DB
    existing_emails = set(u.email for u in local_db.query(AuthUser).all())
    
    # Copy each user (skip if already exists)
    migrated_users_count = 0
    for user in supabase_users:
        if user.email in existing_emails:
            print(f"⊘ Skipped (exists): {user.email}")
            continue
            
        try:
            new_user = AuthUser(
                email=user.email,
                name=user.name,
                avatar_url=user.avatar_url,
                password_hash=user.password_hash
            )
            new_user.id = user.id  # Preserve original ID
            local_db.add(new_user)
            print(f"✓ Migrated: {user.email}")
            migrated_users_count += 1
        except Exception as e:
            print(f"✗ Error migrating {user.email}: {e}")
    
    migrated_rooms_count = 0
    for room in supabase_rooms:
        try:
            new_room = Room(
                name=room.name,
                pax=room.pax,
                level=room.level,
                status=room.status,
                note=room.note,
                image_path=room.image_path,
                until=room.until,
                activeTime=room.activeTime,
                created_at=room.created_at,
                updated_at=room.updated_at,
                created_by=room.created_by,
                updated_by=room.updated_by
            )
            new_room.id = room.id  # Preserve original ID
            local_db.add(new_room)
            print(f"✓ Migrated room: {room.name}")
            migrated_rooms_count += 1
        except Exception as e:
            print(f"✗ Error migrating room {room.name}: {e}")
    
    local_db.commit()
    
    # Verify
    local_users = local_db.query(AuthUser).all()
    local_rooms = local_db.query(Room).all()
    print()
    print(f"✅ Migration complete!")
    print(f"   • Migrated: {migrated_users_count} users")
    print(f"   • Migrated: {migrated_rooms_count} rooms")
    print(f"   • Total in local DB: {len(local_users)} users")
    print(f"   • Total in local DB: {len(local_rooms)} rooms")
    
finally:
    supabase_db.close()
    local_db.close()
