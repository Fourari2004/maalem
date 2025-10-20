# Deploy Your Site to the Internet

This guide will help you deploy your Maalem site so it can be accessed from anywhere on the internet, not just your local WiFi network.

## Deployment Options

We'll use:
1. **Render** for the backend (Django API)
2. **Vercel** for the frontend (React)

Both services offer free tiers that are perfect for your project.

## Prerequisites

1. GitHub account (create one at https://github.com if you don't have one)
2. Render account (create one at https://render.com)
3. Vercel account (create one at https://vercel.com, can use GitHub login)

## Step 1: Push Your Code to GitHub

1. **Add and commit your changes:**
   ```bash
   git add .
   git commit -m "Prepare for internet deployment"
   ```

2. **Push to GitHub:**
   ```bash
   git push origin main
   ```

   If you haven't set up GitHub yet:
   ```bash
   # Create a new repository on GitHub first, then:
   git remote add origin https://github.com/YOUR_USERNAME/maalem.git
   git branch -M main
   git push -u origin main
   ```

## Step 2: Deploy Backend to Render

1. **Sign in to Render** (https://render.com)

2. **Create a new Web Service:**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Set these options:
     - Name: `maalem-backend`
     - Region: Choose the one closest to you
     - Branch: `main`
     - Root Directory: `maalem-backend`
     - Environment: `Python`
     - Build Command: `chmod +x build.sh && ./build.sh`
     - Start Command: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`

3. **Add Environment Variables:**
   - `SECRET_KEY`: Generate a random secret key
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `.onrender.com`
   - `CORS_ALLOWED_ORIGINS`: Leave empty for now (we'll update this after frontend deployment)
   - Database credentials will be automatically set

4. **Add Database:**
   - In the same form, add a PostgreSQL database
   - Name: `maalem-db`

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment to complete (takes 5-10 minutes)
   - Note your backend URL (will look like: `https://maalem-backend.onrender.com`)

## Step 3: Deploy Frontend to Vercel

1. **Sign in to Vercel** (https://vercel.com, can use GitHub login)

2. **Import Your Project:**
   - Click "New Project"
   - Select your GitHub repository
   - Set these options:
     - Framework Preset: `Vite`
     - Root Directory: `maalem-frontend`
     - Build Command: `npm run build`
     - Output Directory: `dist`

3. **Add Environment Variables:**
   - `VITE_API_URL`: `https://your-backend-url.onrender.com/api`
   - Replace `your-backend-url` with your actual Render backend URL

4. **Deploy:**
   - Click "Deploy"
   - Wait for deployment to complete
   - Note your frontend URL (will look like: `https://your-project.vercel.app`)

## Step 4: Update Backend CORS Settings

1. Go back to your Render dashboard
2. Go to your web service settings
3. Update the `CORS_ALLOWED_ORIGINS` environment variable:
   - Add your Vercel frontend URL: `https://your-project.vercel.app`
4. Click "Save Changes"
5. Redeploy the backend

## Step 5: Test Your Deployment

1. Visit your frontend URL: `https://your-project.vercel.app`
2. Try logging in or registering
3. Check that posts and artisans load correctly
4. Test all functionality

## Important Notes

### Security
- Never commit secret keys or passwords to GitHub
- Use environment variables for all sensitive information
- The free tier has some limitations but is perfect for development

### Limitations of Free Tier
- **Render**: Services may spin down after inactivity (first request might be slow)
- **Vercel**: Generous free tier with reasonable limits
- **Database**: Limited to 1GB storage on free tier

### Updating Your Site
To update your deployed site after making changes:
1. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin main
   ```
2. Render will automatically redeploy the backend
3. Vercel will automatically redeploy the frontend

## Troubleshooting

### If Backend Deployment Fails
1. Check the build logs in Render
2. Ensure all dependencies are in `requirements.txt`
3. Verify the `build.sh` script works

### If Frontend Deployment Fails
1. Check the build logs in Vercel
2. Ensure all dependencies are in `package.json`
3. Verify environment variables are correctly set

### If Site Doesn't Load Properly
1. Check browser console for errors
2. Verify API URLs are correct
3. Check that CORS is properly configured
4. Ensure both services are running

## Alternative: Using Heroku for Backend

If you prefer Heroku instead of Render:

1. Sign up at https://heroku.com
2. Install Heroku CLI
3. Create a new app:
   ```bash
   heroku create your-app-name
   ```
4. Set environment variables:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=.herokuapp.com
   heroku config:set CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
   ```
5. Add PostgreSQL:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```
6. Deploy:
   ```bash
   git subtree push --prefix maalem-backend heroku main
   ```

## Support

If you encounter any issues:
1. Check the deployment logs on Render/Vercel
2. Verify all environment variables are set correctly
3. Ensure your GitHub repository is properly configured
4. Contact support on Render/Vercel if needed

Your site will be accessible to anyone on the internet once deployed!