# VOLEXAI - Django LLM Gateway

A multi-provider LLM gateway built with Django, supporting multiple AI providers including OpenAI, Claude, Gemini, Groq, and more.

## Features

- 🔐 Firebase Authentication
- 🤖 Multiple LLM Providers (OpenAI, Claude, Gemini, Groq, etc.)
- 💳 Stripe Payment Integration
- 📊 Token Usage Tracking
- 🔑 API Key Management
- 💬 Chat Session Management

## Tech Stack

- Django 5.2.11
- Django REST Framework
- PostgreSQL
- Firebase Admin SDK
- Multiple LLM Provider SDKs

## Deployment to Render

### Prerequisites

1. A Render account ([sign up here](https://render.com))
2. A GitHub account with this repository
3. Firebase project credentials
4. API keys for LLM providers you want to use

### Step-by-Step Deployment

#### 1. Push Code to GitHub

The code is already pushed to: `https://github.com/kunamvamsikrishna/volexai.git`

#### 2. Create PostgreSQL Database on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "PostgreSQL"
3. Configure:
   - **Name**: `volexai-db`
   - **Database**: `volexai`
   - **User**: `volexai`
   - **Region**: Choose closest to you
   - **Plan**: Free or Starter
4. Click "Create Database"
5. **Copy the Internal Database URL** (you'll need this)

#### 3. Create Web Service on Render

1. Click "New +" → "Web Service"
2. Connect your GitHub repository: `kunamvamsikrishna/volexai`
3. Configure:
   - **Name**: `volexai`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn core.wsgi:application`
   - **Plan**: Free or Starter

#### 4. Add Environment Variables

In the "Environment" section, add ALL these variables:

##### Required Django Settings
```
SECRET_KEY=<generate-a-strong-random-key>
DEBUG=False
DATABASE_URL=<paste-your-render-postgres-internal-url>
ALLOWED_HOSTS=<your-app-name>.onrender.com
```

##### Firebase (Required)
```
FIREBASE_API_KEY=<your-firebase-api-key>
```

##### Google OAuth (if using)
```
GOOGLE_CLIENT_ID=<your-google-client-id>
GOOGLE_CLIENT_SECRET=<your-google-client-secret>
GOOGLE_REDIRECT_URI=https://<your-app-name>.onrender.com/auth/google/callback
GOOGLE_OAUTH_TOKEN_URL=https://oauth2.googleapis.com/token
```

##### LLM Provider API Keys (add only the ones you need)
```
OPENAI_API_KEY=<your-openai-key>
CLAUDE_API_KEY=<your-claude-key>
GEMINI_API_KEY=<your-gemini-key>
GROQ_API_KEY=<your-groq-key>
QUBRID_API_KEY=<your-qubrid-key>
OPENROUTER_API_KEY=<your-openrouter-key>
TOGETHERAI_API_KEY=<your-togetherai-key>
REPLICATE_API_KEY=<your-replicate-key>
HUGGINGFACE_API_KEY=<your-huggingface-key>
CLARIFAI_PAT=<your-clarifai-token>
```

##### Stripe Payment (if using)
```
STRIPE_SECRET_KEY=<your-stripe-secret-key>
STRIPE_WEBHOOK_SECRET=<your-stripe-webhook-secret>
```

#### 5. Upload Firebase Service Account Key

**Important**: You need to upload `firebase_key.json` to Render.

**Option A: Using Render Secret Files**
1. In your Render service settings, go to "Secret Files"
2. Add a new secret file:
   - **Filename**: `firebase_key.json`
   - **Content**: Paste your Firebase service account JSON

**Option B: Using Environment Variable**
1. Convert your `firebase_key.json` to a single-line string
2. Add as environment variable `FIREBASE_CREDENTIALS`
3. Update `authentication/firebase.py` to load from environment variable

#### 6. Deploy

1. Click "Create Web Service"
2. Render will automatically:
   - Clone your repository
   - Run `build.sh` (install dependencies, collect static files, migrate database)
   - Start your application with gunicorn

#### 7. Monitor Deployment

- Watch the deployment logs for any errors
- First deployment may take 5-10 minutes
- Once deployed, your app will be available at: `https://<your-app-name>.onrender.com`

### Post-Deployment

#### Create Superuser

Connect to your Render service shell and create an admin user:

```bash
python manage.py createsuperuser
```

#### Verify

1. Visit `https://<your-app-name>.onrender.com/admin/`
2. Test authentication endpoints
3. Verify LLM provider integrations

### Troubleshooting

#### Static Files Not Loading
- Ensure `whitenoise` is in requirements.txt
- Check that `STATIC_ROOT` is set in settings.py
- Verify `collectstatic` ran successfully in build logs

#### Database Connection Issues
- Verify `DATABASE_URL` environment variable is correct
- Ensure database and web service are in the same region
- Check that migrations ran successfully

#### Firebase Authentication Errors
- Verify `firebase_key.json` is uploaded correctly
- Check `FIREBASE_API_KEY` environment variable
- Ensure Firebase project is active

#### LLM Provider Errors
- Verify API keys are correct
- Check provider-specific rate limits
- Review application logs on Render

### Environment Variables Quick Reference

Copy your `.env` file locally and transfer each variable to Render's environment settings.

### Scaling

- **Free Tier**: App spins down after 15 minutes of inactivity
- **Paid Tier**: Always on, auto-scaling available
- **Database**: Upgrade PostgreSQL plan for more storage/connections

### Security Checklist

✅ `DEBUG=False` in production
✅ Strong `SECRET_KEY` generated
✅ `firebase_key.json` not in git repository
✅ `.env` file not in git repository
✅ All API keys stored as environment variables
✅ `ALLOWED_HOSTS` configured
✅ HTTPS enforced (automatic on Render)

## Local Development

1. Clone the repository
2. Create virtual environment: `python -m venv myenv`
3. Activate: `myenv\Scripts\activate` (Windows) or `source myenv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your values
6. Add your `firebase_key.json` to project root
7. Run migrations: `python manage.py migrate`
8. Start server: `python manage.py runserver`

## API Documentation

Visit `/admin/` for Django admin interface.

## Support

For issues or questions, please open an issue on GitHub.

## License

[Your License Here]
