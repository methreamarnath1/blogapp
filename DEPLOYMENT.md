# Django Blog App - Render Deployment Guide

## Database Choice
Choose your deployment path:
- **SQLite (Simple)**: Keep your current setup. Quick deployment, but data resets when app restarts
- **PostgreSQL (Production)**: More complex setup, but data persists. Recommended for real apps

## Prerequisites
- GitHub account with your Django project pushed
- Render account (https://render.com)
- PostgreSQL database (Render provides this)

## Step-by-Step Deployment

### 1. Initialize Git Repository (if not already done)
```bash
cd BlogApp
git init
git add .
git commit -m "Initial commit: prepare for Render deployment"
git remote add origin https://github.com/YOUR_USERNAME/your-repo-name.git
git branch -M main
git push -u origin main
```

### 2. Create a Render Web Service

1. Go to https://dashboard.render.com
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Select the repository and branch (main)

### 3. Configure the Web Service

**Name:** Your app name (e.g., blog-app)

**Environment:** Python 3

**Build Command:** 
```
pip install -r requirements.txt
```

**Start Command:**
```
gunicorn BlogApp.wsgi:application
```

### 4. Add Environment Variables

In the Render dashboard, add these environment variables:

- **SECRET_KEY**: Generate a new Django secret key at https://djecrety.ir/
- **DEBUG**: False
- **ALLOWED_HOSTS**: your-app-name.onrender.com
- **DATABASE_URL**: (Optional) Only set if using PostgreSQL. Leave empty for SQLite

### 5. Database Setup (Choose One)

#### **Option A: Keep SQLite (Simpler, Current Setup)**
- SQLite is already configured in your project
- **Do NOT set DATABASE_URL** in environment variables
- Your app will use SQLite automatically
- ⚠️ **Limitation**: Render's file system is ephemeral - data will be lost if the app restarts
- ✅ Good for: Testing, small projects, learning

#### **Option B: Use PostgreSQL (Recommended for Production)**
1. In Render dashboard, click "New +" → "PostgreSQL"
2. Name it (e.g., blog-app-db)
3. Select Free or paid tier
4. Click "Create Database"
5. Copy the connection string and set as **DATABASE_URL** in your Web Service environment variables
- ✅ Data persists across app restarts
- ✅ Better performance and scalability
- ✅ Production-ready

### 6. Deploy

1. Once configured, Render will automatically deploy your app
2. The build.sh script will run: collect static files and run migrations
3. Check the logs in the Render dashboard for any errors

### 7. Verify Deployment

- Visit your app URL: `https://your-app-name.onrender.com`
- Check the Logs tab in Render dashboard for any issues
- Test key functionality (login, blog creation, etc.)

## Important Notes

### Static Files
- WhiteNoise handles static file serving automatically
- Run `python manage.py collectstatic` during deployment (included in build.sh)
- CSS and JavaScript files are compressed and cached

### Media Files
- Currently using local storage (media folder)
- ⚠️ **Render's ephemeral storage**: Uploaded files will be lost when the app restarts
- For persistent uploads, consider using AWS S3 or another cloud storage
- Database data: Use PostgreSQL instead of SQLite for persistence (see Step 5)

**To add S3 support in the future:**
```bash
pip install boto3 django-storages
```
Then update settings.py for AWS storage.

### SQLite vs PostgreSQL

**SQLite (Current):**
- ✅ Simple, no extra setup
- ❌ Data lost on app restart
- ❌ Not ideal for production

**PostgreSQL (Recommended):**
- ✅ Data persists
- ✅ Better performance
- ✅ Production-ready
- Requires Step 5 setup

### Database Migrations
- Migrations run automatically in Procfile release phase
- If migrations fail, check logs and fix the issue before redeploying

### Troubleshooting

**502 Bad Gateway Error:**
- Check logs in Render dashboard
- Verify SECRET_KEY and ALLOWED_HOSTS are set correctly
- Ensure build command completed successfully

**Static Files Not Loading:**
- Confirm STATIC_ROOT and STATIC_URL are correct
- Re-deploy to trigger collectstatic

**Database Connection Error:**
- Verify DATABASE_URL is correct
- Ensure database service is running
- Check if migrations completed

**50X Server Errors:**
- Check Render logs
- Verify DEBUG=False (not False in quotes)
- Ensure all required packages are in requirements.txt

### Local Development

**Using SQLite (Default - same as current setup):**
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

**Using PostgreSQL (Optional):**
```bash
# Install dependencies
pip install -r requirements.txt

# Set up local .env
SECRET_KEY=your-dev-key
DEBUG=True
DATABASE_URL=postgresql://postgres:password@localhost:5432/blogapp

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Environment Variables Checklist

**Required:**
- [ ] SECRET_KEY (generate from djecrety.ir)
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS=your-app-name.onrender.com

**Optional:**
- [ ] DATABASE_URL (only if using PostgreSQL; leave empty for SQLite)

## Useful Render CLI Commands

```bash
# Install Render CLI
npm install -g render

# View logs
render logs --service your-service-id

# Check status
render status --service your-service-id
```

## Next Steps

1. Verify your deployed app works
2. Consider adding automated deployments on GitHub pushes
3. Set up error monitoring (e.g., Sentry)
4. Implement S3 for media storage
5. Set up automated backups for database

Happy deploying! 🚀
