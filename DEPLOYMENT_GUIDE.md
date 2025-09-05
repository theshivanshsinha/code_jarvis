# 🚀 CodeJarvis Backend Deployment Guide

## Render.com Deployment

### 1. Prerequisites

- GitHub repository with your CodeJarvis code
- Render.com account

### 2. Quick Deploy Steps

#### Option A: Using Render.yaml (Recommended)

1. Push your code to GitHub with the `render.yaml` file
2. Connect your GitHub repo to Render
3. Render will automatically detect the configuration
4. Update environment variables in Render dashboard

#### Option B: Manual Configuration

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the following:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn start:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
   - **Environment**: Python 3

### 3. Environment Variables to Set in Render Dashboard

**Required:**

```
FLASK_SECRET=your-secret-key-here
CLIENT_ORIGIN=https://your-frontend-domain.onrender.com
GOOGLE_REDIRECT_URI=https://your-backend-domain.onrender.com/api/auth/google/callback
```

**Optional (but recommended):**

```
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
MONGODB_URI=your-mongodb-connection-string
SENDGRID_API_KEY=your-sendgrid-api-key
EMAIL_PASSWORD=your-email-app-password
SMTP_USERNAME=your-smtp-username
SMTP_PASSWORD=your-smtp-password
```

### 4. Post-Deployment Steps

1. **Update Google OAuth Redirect URI:**

   - Go to Google Cloud Console
   - Update OAuth redirect URI to: `https://your-backend-domain.onrender.com/api/auth/google/callback`

2. **Test Your Deployment:**

   ```bash
   curl https://your-backend-domain.onrender.com/api/health
   ```

3. **Update Frontend Configuration:**
   - Update your frontend to point to the new backend URL

## Other Platforms

### Heroku

```bash
# Install Heroku CLI and login
heroku create your-app-name
git push heroku main
```

### Railway

```bash
# Install Railway CLI
railway login
railway init
railway up
```

## Troubleshooting

### Common Issues:

1. **Gunicorn not found**

   - ✅ Fixed: Added `gunicorn==21.2.0` to requirements.txt

2. **Module not found errors**

   - ✅ Fixed: Created proper `start.py` entry point

3. **Port binding issues**

   - ✅ Fixed: Using `$PORT` environment variable

4. **OAuth redirect mismatch**

   - Update `GOOGLE_REDIRECT_URI` to your production domain

5. **CORS issues**
   - Update `CLIENT_ORIGIN` to your frontend domain

### Debug Commands:

```bash
# Test locally with gunicorn
gunicorn start:application --bind 0.0.0.0:5000 --workers 2

# Check if all dependencies are installed
pip install -r requirements.txt

# Test the app creation
python -c "from start import application; print('App created successfully')"
```

## Production Checklist

- [ ] `gunicorn` added to requirements.txt
- [ ] `start.py` created as entry point
- [ ] Environment variables configured
- [ ] Google OAuth redirect URI updated
- [ ] CORS origins updated for production
- [ ] MongoDB connection string (if using)
- [ ] Email service credentials (if using)
- [ ] Test deployment with health check endpoint

Your backend should now deploy successfully! 🎉
