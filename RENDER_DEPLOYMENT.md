# 🚀 Deploy Learnova Flask App to Render

## ✨ Why Render?
- **100% FREE** forever (for web services)
- Deploys Flask apps perfectly
- Automatic HTTPS
- Auto-deploy from GitHub
- **Keeps your original beautiful UI!**

---

## 📋 Step-by-Step Deployment

### **Step 1: Update Your GitHub Repository**

The deployment files are ready! Now push them to GitHub:

#### Using GitHub Desktop:
1. Open GitHub Desktop
2. You'll see changes to:
   - `Procfile` (new)
   - `runtime.txt` (new)
   - `requirements.txt` (updated)
   - `app.py` (updated for deployment)
3. Commit message: `Add Render deployment configuration`
4. Click **"Commit to main"**
5. Click **"Push origin"**

✅ Your GitHub repo is now ready for deployment!

---

### **Step 2: Sign Up for Render**

1. Go to: **https://render.com**
2. Click **"Get Started"** or **"Sign Up"**
3. **Sign up with GitHub** (easiest option)
4. Authorize Render to access your repositories

---

### **Step 3: Create a New Web Service**

1. On Render dashboard, click **"New +"** button (top right)
2. Select **"Web Service"**

3. **Connect your repository:**
   - You'll see a list of your GitHub repos
   - Find **"Learnova-v2"**
   - Click **"Connect"**

4. **Configure your service:**

   **Name:** `learnova` (or any name you like)
   
   **Region:** Choose closest to your location
   
   **Branch:** `main`
   
   **Runtime:** `Python 3`
   
   **Build Command:** `pip install -r requirements.txt`
   
   **Start Command:** `gunicorn app:app`
   
   **Instance Type:** `Free`

5. **Scroll down to Environment Variables**

6. **Click "Add Environment Variable"**
   
   **Key:** `GEMINI_API_KEY`
   
   **Value:** Your Gemini API key
   ```
   AIzaSyC4h0rae0h107_dsEg4yb3f1RtBTJxQjbY
   ```
   (Or your new key if you changed it)

7. **Click "Create Web Service"**

---

### **Step 4: Wait for Deployment**

- Render will start building your app
- You'll see logs showing the installation progress
- Takes about **2-5 minutes**
- Look for: "Your service is live 🎉"

---

### **Step 5: Access Your App! 🎉**

Your app will be live at:
```
https://learnova-xxxx.onrender.com
```

The URL will be shown in your Render dashboard.

**Your original beautiful teal/yellow UI will be there!** ✨

---

## 🎯 **Configuration Summary**

```
Repository: Mourya-006/Learnova-v2
Branch: main
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
Instance Type: Free

Environment Variables:
GEMINI_API_KEY = your-api-key-here
```

---

## 💡 **Important Notes**

### **Free Tier Limitations:**
- ✅ Free forever
- ✅ Automatic HTTPS
- ⚠️ App sleeps after 15 minutes of inactivity
- ⚠️ Takes ~30 seconds to wake up on first request

### **To Keep App Awake (Optional):**
Use a service like **UptimeRobot** (free) to ping your app every 10 minutes.

---

## 🔧 **Troubleshooting**

### **Build Failed?**
- Check that `requirements.txt` has all dependencies
- Make sure Python version is correct in `runtime.txt`

### **App Crashes?**
- Check the logs in Render dashboard
- Verify environment variable `GEMINI_API_KEY` is set correctly

### **Can't Find Repository?**
- Make sure repo is **public**
- Reauthorize Render to access GitHub

---

## 🔄 **Updating Your App**

Whenever you make changes:
1. Push to GitHub (via GitHub Desktop)
2. Render automatically redeploys! (takes 2-3 minutes)

---

## 🎨 **What You're Deploying**

Your original Flask app with:
- ✅ Beautiful teal/yellow UI
- ✅ Chat interface (left panel)
- ✅ Feature cards (right panel)
- ✅ Study timer with presets & custom input
- ✅ Quiz generator
- ✅ Topic explainer
- ✅ Study tips
- ✅ Progress tracking
- ✅ All your custom styling!

---

## 🆚 **Render vs Streamlit**

| Feature | Render (Flask) | Streamlit Cloud |
|---------|----------------|-----------------|
| UI | Your original design | Streamlit's layout |
| Free tier | ✅ Yes | ✅ Yes |
| Custom HTML/CSS | ✅ Full control | ❌ Limited |
| Sleep after inactivity | 15 min | Never |
| Best for | Custom UI apps | Data apps/dashboards |

---

## 📞 **Need Help?**

- Render Docs: https://render.com/docs
- Check logs in Render dashboard for errors
- Make sure all files are pushed to GitHub

---

## 🎉 **You're All Set!**

Your beautiful Learnova app will be live with the exact same UI you designed!

Share your Render URL with friends and start studying together! 🚀
