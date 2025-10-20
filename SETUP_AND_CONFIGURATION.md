# Maalem Platform - Setup and Configuration Guide

This document provides detailed instructions for setting up and configuring the Maalem platform, a social marketplace for Moroccan artisans.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Backend Setup](#backend-setup)
3. [Frontend Setup](#frontend-setup)
4. [Database Configuration](#database-configuration)
5. [Environment Variables](#environment-variables)
6. [Running the Application](#running-the-application)
7. [API Endpoints](#api-endpoints)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### Backend Requirements
- Python 3.8 or higher
- PostgreSQL 12 or higher
- Redis (for real-time features)
- pip (Python package manager)

### Frontend Requirements
- Node.js 16 or higher
- npm or yarn package manager

## Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd maalem-backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create the database schema by running the SQL script:
   ```bash
   # Connect to your PostgreSQL database and run DATABASE_SCHEMA.sql
   ```

## Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd maalem-frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

## Database Configuration

The platform uses PostgreSQL as its database. You need to:

1. Install PostgreSQL on your system
2. Create a database for the application:
   ```sql
   CREATE DATABASE maalem_db;
   CREATE USER maalem_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE maalem_db TO maalem_user;
   ```

3. Run the database schema script to create all tables:
   ```bash
   psql -U maalem_user -d maalem_db -f DATABASE_SCHEMA.sql
   ```

## Environment Variables

### Backend Environment Variables (.env file in maalem-backend/)

Create a `.env` file in the `maalem-backend` directory with the following variables:

```env
# Django settings
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# CORS settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Database settings
DB_NAME=maalem_db
DB_USER=maalem_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Email settings (optional)
EMAIL_HOST=smtp.your-email-provider.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password

# Redis settings (for real-time features)
REDIS_URL=redis://localhost:6379/0

# AWS S3 settings (for media storage - optional)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=your-region
```

### Frontend Environment Variables (.env file in maalem-frontend/)

Create a `.env` file in the `maalem-frontend` directory with the following variables:

```env
# API URL
VITE_API_URL=http://localhost:8000/api
```

## Running the Application

### Starting the Backend

1. Make sure your virtual environment is activated
2. Navigate to the backend directory
3. Run database migrations:
   ```bash
   python manage.py migrate
   ```
4. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```
5. Start the development server:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

### Starting the Frontend

1. Navigate to the frontend directory
2. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

### Starting Redis (for real-time features)

1. Install Redis on your system
2. Start the Redis server:
   ```bash
   redis-server
   ```

## API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/logout/` - User logout

### Users
- `GET /api/users/` - List all users
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user details
- `GET /api/users/artisans/` - List all artisans
- `GET /api/users/me/` - Get current user details

### Posts
- `GET /api/posts/` - List all posts
- `POST /api/posts/` - Create a new post
- `GET /api/posts/{id}/` - Get post details
- `PUT /api/posts/{id}/` - Update post
- `DELETE /api/posts/{id}/` - Delete post
- `POST /api/posts/{id}/like/` - Like/unlike a post
- `POST /api/posts/{id}/add_comment/` - Add a comment to a post
- `POST /api/posts/{id}/share/` - Share a post
- `POST /api/posts/{id}/save_post/` - Save/unsave a post

### Conversations
- `GET /api/conversations/` - List user conversations
- `POST /api/conversations/` - Create a new conversation
- `GET /api/conversations/{id}/` - Get conversation details
- `DELETE /api/conversations/{id}/` - Delete conversation

### Messages
- `GET /api/messages/` - List messages
- `POST /api/messages/` - Send a new message
- `GET /api/messages/{id}/` - Get message details

### Notifications
- `GET /api/notifications/` - List user notifications
- `PUT /api/notifications/{id}/read/` - Mark notification as read

## Troubleshooting

### Common Issues

1. **Database connection errors**
   - Check that PostgreSQL is running
   - Verify database credentials in `.env` file
   - Ensure the database and user exist

2. **Module not found errors**
   - Make sure all dependencies are installed
   - Check that you're in the correct virtual environment

3. **CORS errors**
   - Verify `CORS_ALLOWED_ORIGINS` in the backend `.env` file
   - Ensure the frontend URL is included

4. **Redis connection errors**
   - Check that Redis is running
   - Verify Redis URL in the backend settings

5. **Static files not loading**
   - Run `python manage.py collectstatic` in production
   - Check `STATIC_URL` and `STATIC_ROOT` settings

### Development Tips

1. **Debugging**
   - Set `DEBUG=True` in the backend `.env` file during development
   - Use Django Debug Toolbar for performance analysis

2. **Database migrations**
   - Always create migrations after model changes:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

3. **Frontend development**
   - The frontend uses Vite for hot reloading
   - Component files are in `src/components/`
   - Page files are in `src/pages/`
   - Service files are in `src/services/`

4. **API testing**
   - Use tools like Postman or curl to test API endpoints
   - Authentication tokens are required for most endpoints

## Production Deployment

For production deployment, consider:

1. **Security**
   - Use HTTPS
   - Set `DEBUG=False`
   - Use strong secret keys
   - Implement proper authentication and authorization

2. **Performance**
   - Use a production web server (Nginx, Apache)
   - Implement caching
   - Use a CDN for static assets
   - Optimize database queries

3. **Monitoring**
   - Set up logging
   - Monitor server resources
   - Implement error tracking

4. **Backup**
   - Regular database backups
   - Backup user uploaded media
   - Version control for code changes

This concludes the setup and configuration guide for the Maalem platform. For additional support, refer to the individual README files in each directory.