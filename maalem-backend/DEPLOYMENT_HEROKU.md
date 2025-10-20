# Deployment Guide: Backend to Heroku

This guide will walk you through deploying the Maalem backend to Heroku.

## Prerequisites

1. A Heroku account (free tier available)
2. Heroku CLI installed
3. Git installed
4. PostgreSQL database (can be Heroku Postgres add-on)

## Step-by-Step Deployment

### 1. Prepare Your Repository

Ensure your code is pushed to GitHub:
```bash
git add .
git commit -m "Prepare for Heroku deployment"
git push origin main
```

### 2. Install Heroku CLI

If you haven't already, install the Heroku CLI from [https://devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)

### 3. Log in to Heroku

```bash
heroku login
```

### 4. Create a Heroku App

```bash
heroku create your-app-name
```

Or create through the Heroku dashboard and add the Git remote:
```bash
heroku git:remote -a your-app-name
```

### 5. Set Environment Variables

Set the required environment variables:
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ALLOWED_HOSTS=.herokuapp.com,your-custom-domain.com
heroku config:set CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

### 6. Add PostgreSQL Database

Add the Heroku Postgres add-on:
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

This will automatically set the DATABASE_URL environment variable.

### 7. Update Database Settings

The [settings.py](file:///c%3A/Users/Igolan/Desktop/site%20maalem/maalem-backend/config/settings.py) file is already configured to use the DATABASE_URL environment variable, so no changes are needed.

### 8. Add Redis for Channels

Add the Heroku Redis add-on:
```bash
heroku addons:create heroku-redis:hobby-dev
```

Update the [settings.py](file:///c%3A/Users/Igolan/Desktop/site%20maalem/maalem-backend/config/settings.py) file to use the Redis URL:
```bash
heroku config:set REDIS_URL=$(heroku config:get REDIS_URL)
```

### 9. Create a Procfile

The Procfile should already exist with the following content:
```
release: python manage.py migrate
web: gunicorn config.wsgi
worker: python manage.py runworker channels
```

### 10. Deploy to Heroku

Deploy your application:
```bash
git push heroku main
```

### 11. Run Migrations

If you haven't already, run the migrations:
```bash
heroku run python manage.py migrate
```

### 12. Create a Superuser (Optional)

Create an admin user:
```bash
heroku run python manage.py createsuperuser
```

## Environment Variables

The following environment variables need to be set on Heroku:

| Variable | Description | Example |
|----------|-------------|---------|
| DEBUG | Django debug mode | False |
| SECRET_KEY | Django secret key | your-secret-key |
| ALLOWED_HOSTS | Hosts allowed to serve the app | .herokuapp.com,your-domain.com |
| CORS_ALLOWED_ORIGINS | Frontend URLs allowed to make requests | https://your-frontend.vercel.app |
| DATABASE_URL | PostgreSQL database URL | (Set automatically by Heroku Postgres) |
| REDIS_URL | Redis URL for channels | (Set automatically by Heroku Redis) |

## Custom Domain Setup (Optional)

To use a custom domain:

1. In your Heroku dashboard, go to Settings > Domains
2. Add your custom domain
3. Configure your DNS provider with the CNAME record provided by Heroku

## Troubleshooting

### Deployment Issues

If you encounter deployment issues:

1. Check the build logs: `heroku logs --tail`
2. Ensure all dependencies are in [requirements.txt](file:///c%3A/Users/Igolan/Desktop/site%20maalem/maalem-backend/requirements.txt)
3. Make sure the Procfile is correctly configured

### Database Connection Issues

If you have database connection issues:

1. Verify the DATABASE_URL environment variable is set
2. Check that the Heroku Postgres add-on is installed
3. Ensure migrations have been run

### CORS Issues

If the frontend can't connect to the backend:

1. Verify CORS_ALLOWED_ORIGINS includes your frontend URL
2. Check that the corsheaders middleware is installed and configured
3. Ensure the frontend URL matches exactly (including https://)

## Redeployment

To redeploy after making changes:
```bash
git add .
git commit -m "Description of changes"
git push heroku main
```