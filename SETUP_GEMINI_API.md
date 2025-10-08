# 🔑 Setting Up Gemini API Key

## Step 1: Get Your API Key

1. Go to **Google AI Studio**: https://aistudio.google.com/app/apikey
2. Click **"Get API Key"** or **"Create API Key"**
3. Copy your API key (it looks like: `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`)

## Step 2: Set the API Key

### Option A: Windows PowerShell (Temporary - Current Session Only)

```powershell
$env:GEMINI_API_KEY="your-api-key-here"
python app.py
```

### Option B: Windows Command Prompt (Temporary - Current Session Only)

```cmd
set GEMINI_API_KEY=your-api-key-here
python app.py
```

### Option C: Create a .env File (Permanent - Recommended)

1. Create a file named `.env` in the `Learnova-v2` folder
2. Add this line to the file:
```
GEMINI_API_KEY=your-api-key-here
```
3. Install python-dotenv:
```powershell
pip install python-dotenv
```

### Option D: Windows System Environment Variable (Permanent)

1. Press **Windows Key + R**
2. Type `sysdm.cpl` and press Enter
3. Go to **Advanced** tab → **Environment Variables**
4. Under **User variables**, click **New**
5. Variable name: `GEMINI_API_KEY`
6. Variable value: Your API key
7. Click **OK** on all windows
8. **Restart your terminal/VS Code**

## Step 3: Verify It Works

Run the app and look for this message:
```
✅ Gemini AI successfully initialized with gemini-flash-latest!
```

Instead of:
```
⚠️  WARNING: GEMINI_API_KEY not set!
```

## Quick Test

After setting the API key:
1. Restart the Flask app
2. Open http://127.0.0.1:5001
3. Type "Hello" in the chat
4. You should get an AI-powered response! 🤖

## Troubleshooting

### "API key not found"
- Make sure you copied the complete key
- No spaces before or after the key
- Restart your terminal/VS Code after setting

### "API key invalid"
- Get a new key from Google AI Studio
- Make sure your Google account has access to Gemini API

### Still using fallback mode?
- Check if the environment variable is set: `echo $env:GEMINI_API_KEY` (PowerShell)
- Restart the Python app after setting the key
- Check the terminal output for error messages

## Security Note 🔒

⚠️ **Never commit your API key to GitHub!**
- Add `.env` to your `.gitignore` file
- Keep your API key secret
- Don't share it publicly

---

Need help? Check the console output when starting the app - it will tell you if the API key is detected or not!
