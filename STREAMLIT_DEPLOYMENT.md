# 🚀 Deploy Learnova to Streamlit Cloud

## ✨ Why Streamlit Cloud?
- **100% FREE** forever
- Deploy directly from GitHub
- Automatic HTTPS
- No credit card required
- Perfect for Python apps

---

## 📋 Step-by-Step Deployment Guide

### **Step 1: Push Your Code to GitHub**

1. **Open PowerShell** and navigate to your project:
```powershell
cd d:\Code\Learnova-v2
```

2. **Initialize Git repository:**
```powershell
git init
git add .
git commit -m "Initial commit - Learnova Streamlit version"
```

3. **Create a new repository on GitHub:**
   - Go to https://github.com/new
   - Repository name: `learnova` (or any name you like)
   - Description: "AI-powered study buddy with Gemini"
   - Make it **Public** (required for free Streamlit Cloud)
   - **DO NOT** check "Initialize with README"
   - Click **"Create repository"**

4. **Push your code to GitHub:**
```powershell
git remote add origin https://github.com/YOUR_USERNAME/learnova.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

### **Step 2: Deploy on Streamlit Cloud**

1. **Sign up for Streamlit Cloud:**
   - Go to https://streamlit.io/cloud
   - Click **"Sign up"** or **"Get started"**
   - Sign in with your **GitHub account** (this connects everything automatically)

2. **Create a new app:**
   - Click **"New app"** button
   - You'll see three fields:

   **Repository:** Select `YOUR_USERNAME/learnova`
   
   **Branch:** `main`
   
   **Main file path:** `streamlit_app.py`

3. **Click "Deploy!"**

---

### **Step 3: Add Your Gemini API Key**

⚠️ **IMPORTANT:** Don't hardcode your API key in the code!

1. **Before the app finishes deploying**, click on **"Advanced settings"** or the **⚙️ Settings** icon

2. Go to **"Secrets"** section

3. Add your secret in TOML format:
```toml
GEMINI_API_KEY = "AIzaSyC4h0rae0h107_dsEg4yb3f1RtBTJxQjbY"
```

4. Click **"Save"**

5. The app will automatically redeploy with your API key

---

### **Step 4: Access Your Live App! 🎉**

Your app will be live at:
```
https://YOUR_USERNAME-learnova.streamlit.app
```

Or a similar URL like:
```
https://learnova-xyz123.streamlit.app
```

**Share this URL with anyone!** They can use Learnova for free! 🚀

---

## 🔄 How to Update Your Deployed App

After making changes to your code:

```powershell
cd d:\Code\Learnova-v2
git add .
git commit -m "Your update message"
git push
```

Streamlit Cloud will **automatically detect the changes** and redeploy your app within 1-2 minutes!

---

## 📊 Managing Your App

### View App Dashboard:
- Go to https://share.streamlit.io/
- Sign in with GitHub
- You'll see all your deployed apps

### App Controls:
- **Reboot app:** Restart the app
- **Delete app:** Remove the deployment
- **View logs:** See real-time logs and errors
- **Analytics:** View usage statistics

---

## ⚙️ Streamlit Cloud Features

### Free Tier Includes:
- ✅ 1 GB RAM per app
- ✅ 1 CPU core
- ✅ Unlimited deployments
- ✅ Custom domain support
- ✅ HTTPS automatically enabled
- ✅ Community support

### Limitations:
- Apps sleep after 7 days of inactivity (wake up on first visit)
- Public repositories only for free tier
- 3 app limit on free tier

---

## 🔐 Security Best Practices

1. **Never commit secrets:**
   - `.gitignore` already excludes `.env` files
   - Always use Streamlit Secrets for API keys

2. **Update secrets:**
   - Go to app settings on Streamlit Cloud
   - Edit secrets anytime without redeploying

3. **Monitor API usage:**
   - Check Gemini API usage at https://makersuite.google.com
   - Free tier has daily limits

---

## 🐛 Troubleshooting

### App won't start?
- Check logs in Streamlit Cloud dashboard
- Verify `requirements.txt` has all dependencies
- Ensure `streamlit_app.py` exists and has no syntax errors

### API not working?
- Verify secret is added: `GEMINI_API_KEY`
- Check API key is valid at https://makersuite.google.com
- Review logs for error messages

### App is slow?
- Free tier has limited resources
- Consider optimizing code with `@st.cache_data` and `@st.cache_resource`

### Import errors?
- Add missing packages to `requirements.txt`
- Push changes to GitHub
- Streamlit will auto-redeploy

---

## 🎯 Your Deployment Checklist

- [ ] Code pushed to GitHub (public repository)
- [ ] Signed up for Streamlit Cloud with GitHub
- [ ] Created new app pointing to your repository
- [ ] Added `GEMINI_API_KEY` to Secrets
- [ ] App deployed successfully
- [ ] Tested all features on live URL
- [ ] Shared URL with friends!

---

## 🌟 Next Steps

1. **Custom Domain (Optional):**
   - Go to app settings
   - Add custom domain (requires DNS configuration)

2. **Analytics:**
   - Monitor app usage in Streamlit Cloud dashboard
   - See how many people use your app

3. **Improvements:**
   - Add more features
   - Push to GitHub
   - Auto-deploys in minutes!

---

## 📞 Need Help?

- **Streamlit Docs:** https://docs.streamlit.io/
- **Streamlit Forum:** https://discuss.streamlit.io/
- **Gemini API Docs:** https://ai.google.dev/docs

---

## 🎉 Congratulations!

Your Learnova app is now live and accessible to anyone in the world!

**Your URL:** `https://YOUR_USERNAME-learnova.streamlit.app`

Share it on social media, with classmates, or anyone who wants an AI study buddy! 🚀📚

Made with ❤️ using Streamlit & Google Gemini AI
