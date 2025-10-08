# 🚀 Quick Start - Enable Gemini API

## Fastest Way (3 Steps):

### 1️⃣ Get Your API Key
Visit: **https://aistudio.google.com/app/apikey**
- Sign in with your Google account
- Click "Create API Key" 
- Copy the key (starts with `AIza...`)

### 2️⃣ Set the API Key

**Option A: Use the Setup Script (Easiest)**
```cmd
setup_api_key.bat
```
Then paste your API key when prompted.

**Option B: Manual .env File**
1. Create a file named `.env` in the Learnova-v2 folder
2. Add this line:
```
GEMINI_API_KEY=AIzaSy...your-actual-key...
```
3. Save the file

**Option C: Set Environment Variable (Current Session)**
```powershell
$env:GEMINI_API_KEY="AIzaSy...your-actual-key..."
```

### 3️⃣ Restart the App
```powershell
python app.py
```

## ✅ Success Indicators

You should see:
```
✅ Gemini AI successfully initialized with gemini-flash-latest!
```

Instead of:
```
⚠️  WARNING: GEMINI_API_KEY not set!
```

## 🎉 Test It Out

1. Open http://127.0.0.1:5001
2. Type: "Hello, are you working?"
3. You should get an AI-powered response!
4. Try uploading an image with the 📎 button
5. Ask: "What's in this image?"

## 🆘 Troubleshooting

**Still seeing "API key not set"?**
- Double-check the key has no extra spaces
- Make sure the .env file is in the Learnova-v2 folder
- Restart VS Code or your terminal
- Try running: `Get-Content .env` to verify the file

**"Invalid API key" error?**
- Get a fresh key from Google AI Studio
- Make sure you copied the entire key
- Check your Google account has Gemini API access

**Need help?**
See the full guide: `SETUP_GEMINI_API.md`

---

💡 **Pro Tip**: Keep your API key secret! Never share it or commit it to GitHub.
