# PostgreSQL Setup Guide for Render

## Problem
Projects keep disappearing on Render because the database is not properly configured to use PostgreSQL. The app may be falling back to SQLite which is reset every time the service restarts.

## Solution: Enable PostgreSQL on Render

### Step 1: Create PostgreSQL Database on Render
1. Go to [render.com dashboard](https://dashboard.render.com)
2. Click **New +** → **PostgreSQL**
3. Fill in the details:
   - **Name**: `portfolio-pro-db` (or similar)
   - **Database**: `portfolio_pro`
   - **User**: `portfolio_user` (or your choice)
   - **Region**: Choose same region as your web service
   - **PostgreSQL Version**: Latest
4. Click **Create Database**
5. Wait for the database to be created (2-5 minutes)
6. **Copy the Internal Database URL** (looks like: `postgresql://user:password@host:5432/dbname`)

### Step 2: Add Database URL to Web Service
1. Go to your **Web Service** on Render
2. Go to **Settings** → **Environment**
3. Add new environment variable:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the PostgreSQL URL from Step 1
4. Click **Save Changes**
5. Your service will auto-redeploy with the new environment variable

### Step 3: Verify PostgreSQL is Connected
After deployment:
1. Check Render logs for any database connection errors
2. You should see messages like:
   ```
   INFO sqlalchemy.engine.Engine BEGIN (implicit)
   INFO sqlalchemy.engine.Engine SELECT ...
   ```
3. If you see `sqlite:///portfolio.db`, the DATABASE_URL is not set

### Step 4: Test Data Persistence
1. Log in to admin panel (`/admin/`)
2. Add a new project
3. Mark it as featured
4. Refresh the page - project should still be there
5. Wait 5 minutes, check again - project should persist
6. If Render restarts the service, project should still exist (proving data is in PostgreSQL)

## Troubleshooting

### Projects still disappearing?
**Check:**
- [ ] DATABASE_URL environment variable is set on Render
- [ ] PostgreSQL database status is "Available" on Render dashboard
- [ ] No connection errors in Render logs
- [ ] URL starts with `postgresql://` not `sqlite://`

### Database Connection Error?
1. Verify the PostgreSQL database is in "Available" state
2. Check that DATABASE_URL is correct (copy-paste from Render)
3. Try redeploying the web service from Render dashboard

### Empty Database After Deployment?
This is normal - the database starts empty. Run migrations:
```bash
# Locally, to backup:
sqlite3 portfolio.db ".dump" > backup.sql

# On Render, the database creates tables automatically on first run
# Just add your projects via admin panel
```

## What Happens Now

✅ **With PostgreSQL Configured:**
- All project data persists across deployments
- Admin user persists
- Contact form submissions save permanently
- No data loss on service restarts

❌ **Without PostgreSQL:**
- SQLite database stored in ephemeral storage
- Data resets every time Render restarts the service
- Projects/contacts disappear randomly

## Database URL Format
Your DATABASE_URL should look like:
```
postgresql://username:password@host:5432/database_name
```

**Example:**
```
postgresql://portfolio_user:abc123xyz@oregon-postgres.render.com:5432/portfolio_pro
```

## Next Steps
1. Create PostgreSQL on Render
2. Add DATABASE_URL to environment variables
3. Redeploy web service
4. Test by adding a project and refreshing after 5 mins
5. If data persists, you're good! 🎉

---

**Questions?** Check Render logs for detailed error messages.
