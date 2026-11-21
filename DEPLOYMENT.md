# Fashionkart Deployment Guide

## Deploy to Render (Free)

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

## Access Your App

After deployment, Render will give you a URL like:
`https://fashionkart.onrender.com`

## Local Development

To run locally with SQLite:
```bash
python app.py
```

Then open http://localhost:5000

## Troubleshooting

If you get database errors:
1. Make sure PostgreSQL is created in Render
2. Check DATABASE_URL environment variable
3. Run seed_production.py to populate data
