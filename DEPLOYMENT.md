# Complete Deployment Guide: Maalem Platform

This guide provides instructions for deploying both the frontend and backend of the Maalem platform to production environments.

## Architecture Overview

The Maalem platform consists of:
1. **Frontend**: React/Vite application (deployed to Vercel)
2. **Backend**: Django REST API (deployed to Heroku)
3. **Database**: PostgreSQL (managed by Heroku)
4. **Real-time Features**: Django Channels with Redis
5. **Media Storage**: AWS S3 or Cloudinary

## Deployment Sequence

For a successful deployment, follow this sequence:

1. Deploy the backend first (Heroku)
2. Update frontend environment variables with backend URL
3. Deploy the frontend (Vercel)
4. Configure custom domains (optional)
5. Test the integration

## Backend Deployment (Heroku)

Follow the detailed instructions in [maalem-backend/DEPLOYMENT_HEROKU.md](file:///c%3A/Users/Igolan/Desktop/site%20maalem/maalem-backend/DEPLOYMENT_HEROKU.md)

Key steps:
- Create Heroku app
- Set environment variables
- Add PostgreSQL and Redis add-ons
- Deploy using Git
- Run migrations

After successful backend deployment, note the URL which will be in the format:
`https://your-app-name.herokuapp.com`

## Frontend Deployment (Vercel)

Follow the detailed instructions in [maalem-frontend/DEPLOYMENT_VERCEL.md](file:///c%3A/Users/Igolan/Desktop/site%20maalem/maalem-frontend/DEPLOYMENT_VERCEL.md)

Key steps:
- Push code to GitHub
- Import project to Vercel
- Set environment variables, including:
  ```
  VITE_API_URL=https://your-app-name.herokuapp.com/api
  ```
- Deploy

## Environment Variables Summary

### Backend (.env)
```
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=.herokuapp.com,your-custom-domain.com
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app

DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_HOST=your-database-host
DB_PORT=5432

# Email settings
EMAIL_HOST=smtp.your-email-provider.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password

# AWS S3 (for media storage)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=your-region
```

### Frontend (.env)
```
VITE_API_URL=https://your-app-name.herokuapp.com/api
```

## Post-Deployment Configuration

### 1. Update CORS Settings

After deploying the frontend, update the backend CORS settings to include your Vercel domain:
```
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-custom-domain.com
```

### 2. Configure Media Storage

For production use, configure AWS S3 or Cloudinary for media storage:

#### AWS S3 Configuration:
1. Create an S3 bucket
2. Configure IAM user with appropriate permissions
3. Update environment variables with AWS credentials

#### Cloudinary Configuration:
1. Create a Cloudinary account
2. Get your Cloudinary URL
3. Update Django settings to use Cloudinary

### 3. Email Configuration

Configure a production email service:
1. Set up an email account for sending notifications
2. Update email settings in the backend environment variables

## Testing the Deployment

After both frontend and backend are deployed:

1. Visit your frontend URL
2. Verify that the homepage loads correctly
3. Check that API calls are working (posts, artisans loading)
4. Test user registration/login if implemented
5. Verify real-time features if applicable

## Custom Domains

### Backend (Heroku)
1. Add domain in Heroku dashboard
2. Configure DNS CNAME record

### Frontend (Vercel)
1. Add domain in Vercel dashboard
2. Configure DNS records as instructed

## Monitoring and Maintenance

### Backend
- Monitor Heroku logs: `heroku logs --tail`
- Set up application performance monitoring
- Regular database backups

### Frontend
- Monitor Vercel analytics
- Set up error tracking (e.g., Sentry)

## Scaling Considerations

### Heroku
- Upgrade from free tier for production use
- Add more dynos as needed
- Monitor resource usage

### Vercel
- Free tier is usually sufficient for small to medium applications
- Consider upgrading for higher usage limits

## Security Considerations

1. Never commit secrets to version control
2. Use environment variables for all sensitive data
3. Keep dependencies updated
4. Regularly review access permissions
5. Implement proper authentication and authorization
6. Use HTTPS for all communications

## Troubleshooting Common Issues

### CORS Errors
- Ensure CORS_ALLOWED_ORIGINS includes your frontend domain
- Check that the URL matches exactly (including https)

### API Connection Failures
- Verify backend URL in frontend environment variables
- Check that the backend is running and accessible
- Ensure no typos in API endpoints

### Database Connection Issues
- Verify database credentials
- Check that the database is running
- Ensure proper network access

### Build Failures
- Check build logs for specific error messages
- Ensure all dependencies are properly declared
- Verify Node.js and Python versions match requirements

## Updating Your Deployment

To deploy new changes:

### Backend
```bash
git add .
git commit -m "Description of changes"
git push heroku main
```

### Frontend
Push to GitHub - Vercel will automatically deploy

For manual deployment:
```bash
# If using Vercel CLI
vercel --prod
```