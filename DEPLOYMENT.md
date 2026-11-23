# Fashionkart Deployment Guide

## Option 1: Deploy to Replit (Free - Recommended)

### Step 1: Create Replit Account

1. Go to [replit.com](https://replit.com)
2. Sign up for free account

### Step 2: Create New Repl

1. Click "+ Create Repl"
2. Select "Python" template
3. Name it: `fashionkart`
4. Click "Create Repl"

### Step 3: Upload Files

Either:
- **Option A**: Drag and drop all project files to Replit
- **Option B**: Import from GitHub
  - Click "Import from GitHub"
  - Enter: `https://github.com/p34-wev/ecommerce-paltform.git`

### Step 4: Install Dependencies

In the Replit Shell:
```bash
pip install flask flask-cors
```

Note: Don't install psycopg2 - we'll use SQLite

### Step 5: Configure Replit

1. Open `.replit` file (or create it)
2. Add this configuration:

```toml
[[tasks]]
name = "Run Flask App"
command = "python app.py"
```

### Step 6: Run the App

1. Click "Run" button
2. App will start on Replit's internal port
3. Replit automatically provides a public URL

### Step 7: Seed Database

In the Replit Shell:
```bash
python seed.py
```

### Access Your App

Replit will give you a URL like:
`https://fashionkart-username.replit.co`

### Advantages of Replit
- ✅ Completely free
- ✅ SQLite works out of the box
- ✅ No database setup needed
- ✅ Easy to use
- ✅ Built-in IDE
- ✅ Auto-deploys on save

---

## Option 2: Deploy to Render (Paid - No Free Tier)

### Step 1: Push to GitHub

1. Create a new repository on GitHub
2. Run these commands in your project directory:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/fashionkart.git
git push -u origin main
```

### Step 2: Deploy to Render

1. Go to [render.com](https://render.com)
2. Sign up or login
3. Click "New +" button
4. Select "Web Service"
5. Connect your GitHub repository
6. Configure:
   - **Name**: fashionkart
   - **Region**: Singapore (or nearest to you)
   - **Branch**: main
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
7. Click "Advanced" and add a PostgreSQL database
8. Add environment variable:
   - Key: `DATABASE_URL`
   - Value: (Will be auto-filled by Render)
9. Click "Create Web Service"

### Step 3: Seed the Database

After deployment, run the seed script to populate the database:

1. Go to your Render dashboard
2. Open your web service
3. Click "Shell" (if available) or use Render CLI
4. Run: `python seed_production.py`

### Alternative: Use render.yaml

I've included a `render.yaml` file. When you push to GitHub, Render will automatically detect it.

Just connect your GitHub repo to Render and it will deploy automatically!

### Access Your App

After deployment, Render will give you a URL like:
`https://fashionkart.onrender.com`

---

## Option 3: Deploy to Railway (Free Tier)

### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
```

### Step 2: Login to Railway

```bash
railway login
```

### Step 3: Initialize and Deploy

```bash
railway init
railway up
```

### Step 4: Add PostgreSQL Database

1. Go to Railway dashboard
2. Click "New" → "Database" → "PostgreSQL"
3. Copy the DATABASE_URL from variables tab
4. Add to your project's environment variables

### Step 5: Configure Build Settings

In Railway dashboard for your project:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- Add `DATABASE_URL` environment variable

### Step 6: Seed Database

Open Railway shell and run:
```bash
python seed_production.py
```

---

## Option 4: Deploy to PythonAnywhere (Free Beginner Account)

### Step 1: Create Account

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for a free beginner account

### Step 2: Upload Code

1. Go to "Files" tab
2. Upload all your project files
3. Or use git:
   ```bash
   git clone https://github.com/p34-wev/ecommerce-paltform.git
   ```

### Step 3: Configure Web App

1. Go to "Web" tab
2. Click "Add a new web app"
3. Select "Flask"
4. Python version: 3.10+
5. **Path**: `/home/yourusername/ecommerce-paltform`
6. **WSGI file**: `/var/www/yourusername_pythonanywhere_com_wsgi.py`

### Step 4: Install Dependencies

In the Bash console:
```bash
cd ~/ecommerce-paltform
pip install flask flask-cors
```

### Step 5: Use SQLite (No Database Setup Needed)

PythonAnywhere works directly with SQLite - just upload your `ecommerce.db` file or run:
```bash
python seed.py
```

### Step 6: Reload Web App

Click "Reload" button in the Web tab

---

## Option 5: Deploy to Fly.io (Free Credits)

### Step 1: Install Fly CLI

```bash
curl -L https://fly.io/install.sh | sh
```

### Step 2: Login

```bash
fly auth login
```

### Step 3: Launch App

```bash
fly launch
```

Select:
- App name: fashionkart
- Region: Choose nearest
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`

### Step 4: Add PostgreSQL

```bash
fly postgres create
```

Add the DATABASE_URL to your app:
```bash
fly secrets set DATABASE_URL=your_database_url
```

### Step 5: Deploy

```bash
fly deploy
```

---

## Option 6: Heroku (Paid - No Free Tier)

### Step 1: Install Heroku CLI

```bash
npm install -g heroku
```

### Step 2: Login

```bash
heroku login
```

### Step 3: Create App

```bash
heroku create fashionkart
```

### Step 4: Add PostgreSQL

```bash
heroku addons create heroku-postgresql:mini
```

### Step 5: Deploy

```bash
git push heroku main
```

---

## Local Development

To run locally with SQLite:
```bash
python app.py
```

Then open http://localhost:5000

---

## Troubleshooting

### Replit
1. Check that all files are uploaded
2. Ensure dependencies are installed
3. Run seed.py to populate database

### Railway
1. Check environment variables in dashboard
2. Ensure PostgreSQL is attached to your project
3. Check logs in Railway console

### PythonAnywhere
1. Check error logs in Web tab
2. Ensure all dependencies are installed
3. Verify WSGI configuration

### Fly.io
1. Check: `fly logs`
2. Verify secrets: `fly secrets list`
3. Check health status: `fly status`
