# 📦 GitHub Setup Guide for Learnova

## Method 1: GitHub Desktop (Easiest - No Command Line)

### Step 1: Install GitHub Desktop
1. Download from: https://desktop.github.com/
2. Install and sign in with GitHub account
3. If you don't have a GitHub account, create one at: https://github.com/signup

### Step 2: Add Your Project
1. Open GitHub Desktop
2. Click **"File"** → **"Add Local Repository"**
3. Browse to: `d:\Code\Learnova-v2`
4. Click **"Add repository"**

### Step 3: Initialize (if needed)
If you see "This directory does not appear to be a Git repository":
1. Click **"Create a repository"** 
2. Name: `learnova`
3. Click **"Create Repository"**

### Step 4: Commit Your Code
1. All your files will appear in the left panel
2. In the bottom left text box, type: `Initial commit - Learnova`
3. Click **"Commit to main"**

### Step 5: Publish to GitHub
1. Click **"Publish repository"** at the top
2. Repository name: `learnova`
3. Description: "AI-powered study buddy with Gemini"
4. **UNCHECK** "Keep this code private" (must be public for free Streamlit)
5. Click **"Publish Repository"**

### Step 6: Get Your Repository URL
Your repository will be at: `https://github.com/YOUR_USERNAME/learnova`

**✅ Done! Now proceed to Streamlit deployment.**

---

## Method 2: Git Command Line

### Step 1: Install Git
1. Download from: https://git-scm.com/download/win
2. Run installer with default settings
3. Restart VS Code terminal after installation

### Step 2: Configure Git (First time only)
```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 3: Initialize Repository
```powershell
cd d:\Code\Learnova-v2
git init
git add .
git commit -m "Initial commit - Learnova"
```

### Step 4: Create GitHub Repository
1. Go to: https://github.com/new
2. Repository name: `learnova`
3. Description: "AI-powered study buddy with Gemini"
4. **Public** (required for free Streamlit)
5. **DO NOT** check "Add README" or ".gitignore"
6. Click **"Create repository"**

### Step 5: Push to GitHub
```powershell
git remote add origin https://github.com/YOUR_USERNAME/learnova.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

**✅ Done! Your code is on GitHub.**

---

## After GitHub Setup: Deploy to Streamlit

Once your code is on GitHub, follow these steps:

### Step 1: Go to Streamlit Cloud
Visit: https://streamlit.io/cloud

### Step 2: Sign In
Click "Sign in" and use your **GitHub account**

### Step 3: Deploy New App
1. Click **"New app"** 
2. Repository: `YOUR_USERNAME/learnova`
3. Branch: `main`
4. Main file path: `streamlit_app.py`
5. Click **"Deploy"**

### Step 4: Add Your API Key
1. Click **"Advanced settings"** (⚙️) before deploying
2. In the **"Secrets"** section, add:
```toml
GEMINI_API_KEY = "your-actual-gemini-api-key-here"
```
3. Click **"Save"**
4. Click **"Deploy"**

### Step 5: Wait for Deployment
- Takes 2-5 minutes
- You'll get a URL like: `https://YOUR_USERNAME-learnova.streamlit.app`

### Step 6: Share Your App! 🎉
Your Learnova is now live and accessible to anyone!

---

## Troubleshooting

### "Repository not found"
- Make sure repository is **Public** (not Private)
- Check repository name spelling

### "No module named 'streamlit'"
- Check that `requirements.txt` is in the root folder
- Streamlit will automatically install dependencies

### "API Key not working"
- Verify the API key in Secrets section
- Format must be: `GEMINI_API_KEY = "your-key-here"`
- Include the quotes

### "App keeps sleeping"
- Free tier apps sleep after 7 days of inactivity
- Just visit the URL to wake it up

---

## Need Help?

- GitHub Desktop docs: https://docs.github.com/en/desktop
- Streamlit deployment docs: https://docs.streamlit.io/streamlit-community-cloud
- Git tutorial: https://git-scm.com/docs/gittutorial

---

## 🎓 What You've Built

Your Learnova app includes:
- ✅ AI Chat with Gemini
- ✅ Topic Explainer
- ✅ Quiz Generator
- ✅ Study Timer
- ✅ Study Tips
- ✅ Progress Tracking
- ✅ Beautiful Teal/Yellow UI

Share your deployment URL with friends and help them study! 🚀
