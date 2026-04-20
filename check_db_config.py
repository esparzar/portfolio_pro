#!/usr/bin/env python
"""
Database Configuration Checker
Run this to verify your database setup on Render
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_database_config():
    """Check if database is properly configured"""
    
    print("\n" + "="*60)
    print("DATABASE CONFIGURATION CHECKER")
    print("="*60 + "\n")
    
    # Check for DATABASE_URL
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables!")
        print("\n⚠️  ISSUE: Your app is using SQLite (ephemeral storage)")
        print("   Projects will disappear when Render restarts the service.\n")
        print("📝 SOLUTION: Set DATABASE_URL on Render:\n")
        print("   1. Create PostgreSQL database on Render.com")
        print("   2. Copy the connection string")
        print("   3. Add it as DATABASE_URL environment variable")
        print("   4. Redeploy the service\n")
        return False
    
    print("✅ DATABASE_URL is set\n")
    
    # Parse the URL to show what's configured
    if database_url.startswith('postgresql://') or database_url.startswith('postgres://'):
        db_type = "PostgreSQL"
        status = "✅ PRODUCTION READY"
        print(f"Database Type: {db_type}")
        print(f"Status: {status}\n")
        print("✅ Your data WILL persist across deployments!\n")
        
        # Extract host info (don't show password)
        try:
            parts = database_url.split('@')
            if len(parts) > 1:
                host_part = parts[1].split('/')[0]
                db_name = database_url.split('/')[-1]
                print(f"Database Host: {host_part}")
                print(f"Database Name: {db_name}\n")
        except:
            pass
        
        return True
    
    elif 'sqlite' in database_url:
        db_type = "SQLite"
        status = "⚠️  EPHEMERAL (data will be lost)"
        print(f"Database Type: {db_type}")
        print(f"Status: {status}\n")
        print("❌ Your data WILL NOT persist across deployments!\n")
        return False
    
    else:
        print("⚠️  Unknown database type\n")
        return False

if __name__ == '__main__':
    success = check_database_config()
    
    print("="*60)
    if success:
        print("Database configuration looks good! ✅")
        sys.exit(0)
    else:
        print("Database needs to be configured. See instructions above. ⚠️")
        sys.exit(1)
