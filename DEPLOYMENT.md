# Deployment Instructions for Render.com

## Steps to Deploy:

1. **Sign up for Render**: Go to https://render.com and create a free account

2. **Create PostgreSQL Database**:
   - In Render dashboard, click "New +"
   - Select "PostgreSQL"
   - Choose free tier
   - Set name: `demonlist-db`
   - Copy the internal database URL

3. **Create Web Service**:
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository
   - Choose Python environment
   - Set Start Command: `flask init-db && gunicorn app:app`

4. **Set Environment Variables** in Render:
   - `FLASK_APP`: `app.py`
   - `FLASK_ENV`: `production`
   - `DATABASE_URL`: Paste your PostgreSQL database URL from step 2
   - `SECRET_KEY`: Generate a secure random key

5. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Your site will be available at: `https://your-service-name.onrender.com`

6. **Create Admin User**:
   - Once deployed, open a terminal in your project
   - Run: `flask create-admin` or access the admin panel

## Environment Variables for Render:

```
FLASK_APP=app.py
FLASK_ENV=production
DATABASE_URL=postgresql://username:password@your-db-host/demonlist_db
SECRET_KEY=your-secret-key-here
```

## Alternative Hosting Options:

### Railway.app (Recommended - Easier)
1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Connect this repo
5. Add PostgreSQL plugin
6. Set environment variables
7. Deploy!

### Heroku (Legacy but still works)
1. Sign up at https://www.heroku.com
2. Install Heroku CLI
3. Run: `heroku create your-app-name`
4. Add PostgreSQL: `heroku addons:create heroku-postgresql:hobby-dev`
5. Push to Heroku: `git push heroku main`

### PythonAnywhere
1. Go to https://www.pythonanywhere.com
2. Upload your project
3. Configure WSGI app
4. Connect PostgreSQL
5. Reload web app

## Notes:
- Free tier services may have limitations (downtime, limited resources)
- For production use, consider upgrading to paid plans
- Database backups are important for production
