# 🔐 User Authentication Guide

## Overview

Learnova supports **two modes** of operation:

### 🎭 Guest Mode (Default)
- ✅ **No signup required** - Start using immediately
- ✅ **Full AI features** - Chat, file upload, timer, quizzes
- ⚠️ **No progress saving** - Data lost after closing browser
- ⚠️ **No cloud sync** - Can't access from other devices

### 👤 Authenticated Mode
- ✅ **Email/Password Login** - Traditional account creation
- ✅ **Google Sign-In** - Quick login with Google account
- ✅ **Progress saved** - All study sessions and stats saved
- ✅ **Cloud sync** - Access from any device
- ✅ **Profile** - Personalized experience

**You can start as a guest and sign up later to save your progress!**

---

## 🚀 Quick Start

### Option 1: Use as Guest (No Signup)
1. Go to http://127.0.0.1:5001
2. You're already in! 🎉
3. Use all AI features immediately
4. Click "Sign Up" when ready to save progress

### Option 2: Create Account Immediately

#### Option 1: Sign Up with Email
1. Go to http://127.0.0.1:5001/signup
2. Enter your full name, email, and password (min 6 characters)
3. Click "Create Account"
4. You'll be automatically logged in!

#### Option 2: Sign Up with Google
1. Go to http://127.0.0.1:5001/login or /signup
2. Click "Continue with Google" or "Sign up with Google"
3. Choose your Google account
4. Grant permissions
5. Done! You're logged in!

---

## 🔧 Setup Guide for Developers

### 1. Basic Setup (Email/Password Only)

Already working! Just run:
```powershell
cd d:\Code\Learnova-v2
python app.py
```

The database will be automatically created on first run.

### 2. Google OAuth Setup (Optional but Recommended)

To enable Google Sign-In, follow these steps:

#### Step 1: Create Google Cloud Project

1. Go to **[Google Cloud Console](https://console.cloud.google.com/)**
2. Click **"Create Project"** or select existing project
3. Name your project: `Learnova` (or any name)
4. Click **"Create"**

#### Step 2: Enable Google+ API

1. In your project, go to **"APIs & Services"** → **"Library"**
2. Search for **"Google+ API"**
3. Click on it and press **"Enable"**

#### Step 3: Create OAuth 2.0 Credentials

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** → **"OAuth client ID"**
3. If prompted, configure OAuth consent screen:
   - User Type: **External**
   - App name: **Learnova**
   - User support email: Your email
   - Developer contact: Your email
   - Click **"Save and Continue"**
   - Scopes: Click **"Save and Continue"** (keep defaults)
   - Test users: Add your Gmail address
   - Click **"Save and Continue"**

4. Back to Create OAuth client ID:
   - Application type: **Web application**
   - Name: **Learnova Web Client**
   - Authorized redirect URIs: Add these:
     ```
     http://localhost:5001/auth/google/callback
     http://127.0.0.1:5001/auth/google/callback
     ```
   - Click **"Create"**

5. Copy your credentials:
   - **Client ID** (looks like: `123456789-abc.apps.googleusercontent.com`)
   - **Client Secret** (looks like: `GOCSPX-abc123xyz...`)

#### Step 4: Add Credentials to .env File

Open `d:\Code\Learnova-v2\.env` and update:

```env
# Gemini API Key
GEMINI_API_KEY=AIzaSyCsp4ryDvxJ3JvMsxwxs9dVjkzo1YfpD5U

# Secret key for Flask sessions
SECRET_KEY=your-random-secret-key-here

# Google OAuth credentials
GOOGLE_CLIENT_ID=YOUR_CLIENT_ID_HERE
GOOGLE_CLIENT_SECRET=YOUR_CLIENT_SECRET_HERE
```

**Important:** Generate a secure SECRET_KEY:
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```
Copy the output and paste it as your `SECRET_KEY`.

#### Step 5: Restart the Server

```powershell
cd d:\Code\Learnova-v2
python app.py
```

Now Google Sign-In will work! ✅

---

## 🎭 Guest Mode vs Authenticated Mode

### Guest Mode Features:
| Feature | Available |
|---------|-----------|
| Chat with AI | ✅ Yes |
| File Upload | ✅ Yes |
| Study Timer | ✅ Yes |
| Quiz Generation | ✅ Yes |
| Session Stats | ✅ Yes (browser only) |
| Progress Saving | ❌ No (lost on close) |
| Cloud Sync | ❌ No |
| Multi-device Access | ❌ No |
| Profile | ❌ No |

### Authenticated Mode Features:
| Feature | Available |
|---------|-----------|
| All Guest Features | ✅ Yes |
| Progress Saving | ✅ Yes (permanent) |
| Cloud Sync | ✅ Yes |
| Multi-device Access | ✅ Yes |
| Profile Picture | ✅ Yes (Google users) |
| Study History | ✅ Yes |
| Personalization | ✅ Yes |

### When to Sign Up:
- 📚 **Long-term studying** - Want to track progress over weeks/months
- 💾 **Save progress** - Don't want to lose your study data
- 🌐 **Multiple devices** - Access from phone, tablet, and computer
- 📊 **Analytics** - Detailed study statistics and insights

### Why Guest Mode is Great:
- ⚡ **Instant access** - No signup friction
- 🎯 **Try before commit** - Test all features first
- 🔒 **Privacy** - No email required to try
- 🚀 **Quick learning** - Perfect for one-time questions

---

## 📋 Features

### User Profile
- Displays user's name and email
- Shows profile picture (for Google users)
- Avatar placeholder with initial for email users

### Session Management
- Automatic login after signup
- "Remember me" functionality
- Secure session cookies
- Auto-logout after inactivity

### Protected Routes
~~All chat and study features require login~~ **Updated:** All features work in guest mode!

**No login required:**
- `/` - Main app (works for everyone!)
- `/api/chat` - Chat endpoint (guests welcome)
- `/api/save-session` - Study session saving (guests use browser storage)
- `/api/stats` - User statistics (guests see session stats)

**Login-only routes:**
- `/login` - Login page
- `/signup` - Signup page
- `/auth/google` - Google OAuth initiation
- `/auth/google/callback` - Google OAuth callback
- `/api/auth/logout` - Logout endpoint
- `/api/auth/user` - Get user info

---

## 🔐 Security Features

### Password Security
- Passwords hashed with bcrypt (industry standard)
- Minimum 6 characters enforced
- Never stored in plain text

### Session Security
- Secure Flask sessions
- CSRF protection
- HTTPOnly cookies
- Session expiration

### OAuth Security
- Official Google OAuth 2.0
- Encrypted token exchange
- Secure callback handling
- No password storage for OAuth users

### Database Security
- SQLite database (`learnova.db`)
- Email uniqueness enforced
- Indexed queries for performance
- Protected by `.gitignore`

---

## 🎨 UI Features

### Login Page (`/login`)
- Email and password fields
- Google Sign-In button
- Link to signup page
- Black and orange theme

### Signup Page (`/signup`)
- Name, email, password fields
- Password validation (min 6 chars)
- Google Sign-Up button
- Link to login page
- Duplicate email detection

### Main App (after login)
- User profile in header
- Profile picture or initial avatar
- Logout button
- All study features unlocked

---

## 🛠️ API Endpoints

### Authentication Endpoints

#### `POST /api/auth/signup`
Create new account with email/password.

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Account created successfully!",
  "user": {
    "id": 1,
    "email": "john@example.com",
    "name": "John Doe",
    "created_at": "2025-10-09T12:00:00"
  }
}
```

#### `POST /api/auth/login`
Login with email/password.

**Request:**
```json
{
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Login successful!",
  "user": {
    "id": 1,
    "email": "john@example.com",
    "name": "John Doe",
    "last_login": "2025-10-09T12:05:00"
  }
}
```

#### `POST /api/auth/logout`
Logout current user (requires authentication).

**Response:**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

#### `GET /api/auth/user`
Get current logged-in user info (requires authentication).

**Response:**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "email": "john@example.com",
    "name": "John Doe",
    "profile_picture": "https://...",
    "created_at": "2025-10-09T12:00:00",
    "last_login": "2025-10-09T12:05:00"
  }
}
```

---

## 📊 Database Schema

### Users Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| email | String(120) | Unique email address |
| name | String(100) | User's full name |
| password_hash | String(200) | Bcrypt hashed password (null for OAuth users) |
| google_id | String(100) | Google account ID (null for email users) |
| profile_picture | String(500) | URL to profile picture |
| created_at | DateTime | Account creation timestamp |
| last_login | DateTime | Last login timestamp |

---

## 🚨 Troubleshooting

### Google Sign-In Not Working

**Problem:** "Error 400: redirect_uri_mismatch"

**Solution:**
1. Go to Google Cloud Console
2. Navigate to Credentials
3. Edit your OAuth client ID
4. Under "Authorized redirect URIs", add:
   - `http://localhost:5001/auth/google/callback`
   - `http://127.0.0.1:5001/auth/google/callback`
5. Save and wait 5 minutes for changes to propagate

### Database Not Created

**Problem:** No `learnova.db` file

**Solution:**
```powershell
cd d:\Code\Learnova-v2
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database created!')"
```

### Can't Login After Signup

**Problem:** "Invalid email or password"

**Solution:**
- Check email is correct (case-sensitive)
- Password must be at least 6 characters
- Clear browser cookies and try again

### "CSRF Token Missing" Error

**Problem:** CSRF error on form submission

**Solution:**
Make sure `SECRET_KEY` is set in `.env`:
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```
Add output to `.env` as `SECRET_KEY=...`

---

## 🌐 Deployment Notes

### Render.com

Add these environment variables in Render dashboard:

```
GEMINI_API_KEY=your-key-here
SECRET_KEY=your-secret-key-here
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

**Important:** Update Google OAuth redirect URIs with your Render URL:
```
https://your-app.onrender.com/auth/google/callback
```

### Heroku

Add environment variables:
```bash
heroku config:set GEMINI_API_KEY=your-key
heroku config:set SECRET_KEY=your-secret
heroku config:set GOOGLE_CLIENT_ID=your-id
heroku config:set GOOGLE_CLIENT_SECRET=your-secret
```

---

## 📚 Additional Resources

- **Flask-Login Docs:** https://flask-login.readthedocs.io/
- **Google OAuth Setup:** https://developers.google.com/identity/protocols/oauth2
- **Authlib Documentation:** https://docs.authlib.org/
- **Flask-Bcrypt:** https://flask-bcrypt.readthedocs.io/

---

## ✅ Testing Checklist

- [ ] Email signup works
- [ ] Email login works
- [ ] Google sign-in works (if configured)
- [ ] Logout works
- [ ] User profile displays correctly
- [ ] Protected routes require login
- [ ] Chat works after login
- [ ] Study timer works after login
- [ ] Quiz generation works after login

---

**Authentication is now fully integrated!** 🎉

Users must create an account to use Learnova's AI study features. This ensures:
- ✅ Personalized study tracking
- ✅ Secure data storage
- ✅ Progress history
- ✅ Better user experience

For questions or issues, check the troubleshooting section or review the code in:
- `app.py` - Authentication routes
- `models.py` - User database model
- `templates/auth.html` - Login/signup UI
- `templates/index.html` - Main app with user profile
