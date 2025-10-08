# 🚀 Quick GitHub Upload Guide

## ⚡ Fastest Method: GitHub Desktop (No Command Line!)

### 1. Install Git & GitHub Desktop
- Download Git: https://git-scm.com/download/win
- Download GitHub Desktop: https://desktop.github.com/

### 2. Open GitHub Desktop
- Sign in with your GitHub account
- (Create account at https://github.com if needed)

### 3. Add Your Project
1. Click **File** → **Add Local Repository**
2. Choose: `d:\Code\Learnova-v2`
3. If it says "not a Git repository", click **"Create Repository"**

### 4. Publish to GitHub
1. Click **"Publish repository"** button (top)
2. Name: `Learnova-v2`
3. Description: "AI Study Buddy with file upload"
4. Choose **Public** or **Private**
5. Click **"Publish"**

✅ **Done!** Your code is on GitHub!

---

## 🔐 Security Check Before Upload

### Run This Verification Script:
```powershell
cd d:\Code\Learnova-v2
.\verify_security.bat
```

Should show:
- ✅ `.env` is in `.gitignore`
- ✅ `.env` exists locally
- ✅ `.env.example` exists (template for others)

---

## 📋 What Gets Uploaded

### ✅ SAFE (Uploaded):
```
app.py
ai_helper.py
requirements.txt
templates/
static/
.env.example    ← Template only
.gitignore      ← Protection file
README.md
```

### ❌ PROTECTED (Not Uploaded):
```
.env            ← YOUR ACTUAL API KEY!
uploads/
__pycache__/
data/
```

---

## 🔄 After Upload

### Your GitHub URL:
```
https://github.com/YOUR_USERNAME/Learnova-v2
```

### Deploy to Render:
See `RENDER_DEPLOYMENT.md` for instructions!

---

## 🆘 If You Accidentally Upload `.env`

1. **Immediately revoke your API key:**
   - Go to: https://aistudio.google.com/app/apikey
   - Delete the exposed key
   - Generate a new one

2. **Remove from GitHub:**
   ```powershell
   git rm --cached .env
   git commit -m "Remove .env"
   git push
   ```

3. **Update your local `.env` with new key**

---

## 💡 Complete Guides

For detailed instructions, see:
- **`GITHUB_SETUP.md`** - Full GitHub upload guide
- **`GITHUB_VS_RENDER.md`** - How API keys work
- **`SECURITY.md`** - Security best practices

---

**Bottom Line:** Use GitHub Desktop for easy upload. Your `.env` file is automatically protected by `.gitignore`! 🔒✨
