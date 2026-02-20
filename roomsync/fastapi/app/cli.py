#!/usr/bin/env python3
"""
CLI commands for app management
Usage: python -m app.cli migrate
"""
import sys
import click
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load environment
env_file = Path(__file__).resolve().parent.parent / ".env"
if env_file.exists():
    load_dotenv(env_file)

from app.models.authuser import AuthUser
from app.db import Base
import os

@click.group()
def cli():
    """Room Sync Management CLI"""
    pass


@cli.command()
def migrate():
    """Migrate AuthUser data from Supabase to local database"""
    
    SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")
    LOCAL_DB_URL = os.getenv("DATABASE_URL")
    
    if not SUPABASE_DB_URL or not LOCAL_DB_URL:
        click.echo("❌ Error: SUPABASE_DB_URL or DATABASE_URL not set in .env", err=True)
        sys.exit(1)
    
    click.echo(f"📦 Source: {SUPABASE_DB_URL[:40]}...")
    click.echo(f"📦 Destination: {LOCAL_DB_URL[:40]}...")
    
    try:
        supabase_engine = create_engine(SUPABASE_DB_URL, pool_pre_ping=True)
        local_engine = create_engine(LOCAL_DB_URL, pool_pre_ping=True)
        
        SupabaseSession = sessionmaker(bind=supabase_engine)
        LocalSession = sessionmaker(bind=local_engine)
        
        Base.metadata.create_all(local_engine)
        click.echo("✓ Tables ready")
        
        supabase_db = SupabaseSession()
        local_db = LocalSession()
        
        supabase_users = supabase_db.query(AuthUser).all()
        click.echo(f"Found {len(supabase_users)} users\n")
        
        if len(supabase_users) == 0:
            click.echo("✅ No users to migrate")
            return
        
        existing_emails = set(u.email for u in local_db.query(AuthUser).all())
        migrated_count = 0
        
        for user in supabase_users:
            if user.email in existing_emails:
                click.echo(f"  ⊘ Skipped: {user.email}")
                continue
            
            new_user = AuthUser(
                email=user.email,
                name=user.name,
                avatar_url=user.avatar_url,
                password_hash=user.password_hash
            )
            new_user.id = user.id
            local_db.add(new_user)
            click.echo(f"  ✓ Migrated: {user.email}")
            migrated_count += 1
        
        local_db.commit()
        
        local_users = local_db.query(AuthUser).all()
        click.echo()
        click.echo(f"✅ Complete! Migrated {migrated_count}, Total: {len(local_users)}")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)
    finally:
        supabase_db.close()
        local_db.close()


if __name__ == "__main__":
    cli()
