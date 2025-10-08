# 🎓 Learnova - AI-Powered Study Buddy

Learnova is an intelligent study companion that helps you learn more effectively using Google's Gemini AI.

## ✨ Features

- 💬 **AI Chat Assistant** - Ask questions and get helpful explanations
- � **File Upload** - Upload images and documents for AI analysis
- �📚 **Topic Explanations** - Get detailed explanations at different difficulty levels
- 📝 **Quiz Generator** - Create custom quizzes on any topic
- 💡 **Study Tips** - Personalized tips based on your learning style
- ⏱️ **Study Timer** - Pomodoro timer with session tracking
- 📊 **Progress Tracking** - Monitor your study sessions and progress

## 🚀 Quick Start

### 1. Get Your Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### 2. Install Dependencies

```powershell
cd Learnova-v2
pip install -r requirements.txt
```

### 3. Set Your API Key

**Option A: Using .env file (Recommended)**
```powershell
# Create .env file
echo "GEMINI_API_KEY=your-api-key-here" > .env
```

**Option B: Using environment variable**
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
```

**Option C: Using setup script**
```cmd
setup_api_key.bat
```

### 4. Run the App

```powershell
python app.py
```

### 5. Open Learnova

Open your browser and go to: **http://localhost:5001**

## 🔒 Security - IMPORTANT!

⚠️ **NEVER commit your `.env` file to GitHub!**

Your API key is sensitive and should be kept secret:
- ✅ `.env` is already in `.gitignore` (protected)
- ✅ Use `.env.example` as a template
- ✅ Each developer gets their own API key
- ❌ Never share your actual API key
- ❌ Never commit `.env` to version control

**See `SECURITY.md` for detailed security guidelines.**

Before pushing to GitHub:
```powershell
git status  # Verify .env is NOT listed
```

## 🎨 Theme

Learnova features a beautiful **Black & Orange** color scheme:
- Dark gradient background (#181818 to #232526)
- Vibrant orange accents (#ff9800, #ffb300)
- Modern dark theme with smooth animations

## 📁 Project Structure

```
Learnova-v2/
├── app.py              # Flask backend server
├── ai_helper.py        # Gemini AI integration
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # Main UI
├── static/
│   ├── css/
│   │   └── style.css  # Teal/yellow theme
│   └── js/
│       └── app.js     # Frontend logic
└── data/              # User session data
```

## 🔧 Configuration

### Environment Variables

- `GEMINI_API_KEY` - Your Google Gemini API key (required for AI features)

### Difficulty Levels

- **Beginner** - Simple explanations with everyday analogies
- **Intermediate** - Clear explanations with examples
- **Advanced** - Detailed technical explanations

### Learning Styles

- **Visual** - Diagrams, videos, and visual aids
- **Auditory** - Audio resources and discussions
- **Kinesthetic** - Hands-on exercises and practice

## 🛠️ Troubleshooting

### "Gemini API not initialized"

Make sure you've set the API key before starting the app:
```powershell
$env:GEMINI_API_KEY="your-key-here"
python app.py
```

### "Module not found" errors

Install all dependencies:
```powershell
pip install -r requirements.txt
```

### API Key not working

1. Check that your API key is valid at [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Make sure you set it in the same terminal session where you run the app
3. The key should start with "AIzaSy..."

## 📝 Usage Tips

1. **Study Timer**: Use the Pomodoro technique (25 min focus sessions)
2. **Quiz Practice**: Generate quizzes after learning a topic to test your knowledge
3. **Chat**: Ask follow-up questions to deepen your understanding
4. **Difficulty Levels**: Start with beginner and progress to advanced

## 🎯 Made with

- **Backend**: Flask (Python)
- **AI**: Google Gemini Pro
- **Frontend**: HTML5, CSS3, JavaScript
- **Icons**: Font Awesome

## 📄 License

This project is for educational purposes.

---

**Happy Learning! 📚✨**
