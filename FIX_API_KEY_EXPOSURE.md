# 🚨 URGENT: Fix API Key Exposure

GitHub detected your API key in the repository. Here's how to fix it:

## ⚠️ What Happened?
Your Gemini API key was accidentally committed to GitHub in documentation files (STREAMLIT_DEPLOYMENT.md and GITHUB_SETUP.md).

## 🔧 How to Fix (3 Steps)

### Step 1: Delete Your Old API Key and Create a New One

**Your exposed key:** `AIzaSyC4h0rae0h107_dsEg4yb3f1RtBTJxQjbY`

1. Go to **Google AI Studio**: https://makersuite.google.com/app/apikey
2. Click on your existing API key
3. **Delete** or **Revoke** the exposed key
4. Click **"Create API Key"** to generate a new one
5. **Copy the new key** and save it somewhere safe (NOT in the code!)

### Step 2: Update GitHub Repository

I've already removed the API key from the files. Now you need to push the changes:

#### Using GitHub Desktop:
1. Open GitHub Desktop
2. You'll see changes to `STREAMLIT_DEPLOYMENT.md` and `GITHUB_SETUP.md`
3. Commit message: `Remove exposed API key from documentation`
4. Click **"Commit to main"**
5. Click **"Push origin"**

#### Using Git Command Line:
```powershell
cd d:\Code\Learnova-v2
git add .
git commit -m "Remove exposed API key from documentation"
git push
```

### Step 3: Update Streamlit with New API Key

1. Go to your Streamlit app: https://share.streamlit.io/
2. Click on your app → **⚙️ Settings** → **Secrets**
3. Update the secret with your **NEW** API key:
```toml
GEMINI_API_KEY = "your-new-api-key-here"
```
4. Click **"Save"**
5. App will automatically restart with the new key

---

## 🛡️ Security Best Practices

### ✅ DO:
- Store API keys in environment variables or secrets managers
- Use `.gitignore` to prevent sensitive files from being committed
- Use placeholder values in documentation (e.g., `"your-api-key-here"`)
- Rotate keys immediately if exposed

### ❌ DON'T:
- Never hardcode API keys in source code
- Never commit API keys to version control
- Never share API keys in documentation or README files
- Never store keys in plain text files that are tracked by Git

---

## 📋 Verification Checklist

After fixing:
- [ ] Old API key deleted from Google AI Studio
- [ ] New API key created
- [ ] GitHub repository updated (API key removed)
- [ ] Streamlit Secrets updated with new key
- [ ] App tested and working with new key
- [ ] GitHub security alert dismissed/resolved

---

## 🔍 How to Prevent This in the Future

1. **Never put real API keys in documentation**
   - Always use: `"your-api-key-here"` as placeholder

2. **Check before committing**
   - Review files before pushing to GitHub
   - Use `git diff` to see what's being committed

3. **Use .gitignore properly**
   - The `.gitignore` file should prevent `.env` and `secrets.toml` from being committed
   - But documentation files (`.md`) are still tracked!

4. **Use GitHub's Secret Scanning**
   - GitHub automatically scans for exposed secrets
   - Act immediately when you receive alerts

---

## 📞 Need Help?

If you see the GitHub alert:
1. Follow the "Revoke" link in the email
2. Complete the 3 steps above
3. The alert will automatically close once the key is revoked

Your app will continue working once you update Streamlit with the new key!
