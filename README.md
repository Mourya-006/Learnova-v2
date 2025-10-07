# 🎓 Learnova - AI-Powered Study Buddy

Learnova is an intelligent study companion that helps you learn more effectively using Google's Gemini AI.

## ✨ Features

- 💬 **AI Chat Assistant** - Ask questions and get helpful explanations
- 📚 **Topic Explanations** - Get detailed explanations at different difficulty levels
- 📝 **Quiz Generator** - Create custom quizzes on any topic
- 💡 **Study Tips** - Personalized tips based on your learning style
- ⏱️ **Study Timer** - Pomodoro timer with session tracking
- 📊 **Progress Tracking** - Monitor your study sessions and progress

## 🚀 Quick Start

### 1. Get Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### 2. Install Dependencies

```powershell
cd Learnova-v2
pip install -r requirements.txt
```

### 3. Set Your API Key & Run

```powershell
$env:GEMINI_API_KEY="your-api-key-here"
python app.py
```

### 4. Open Learnova

Open your browser and go to: **http://localhost:5000**

## 🎨 Theme

Learnova features a beautiful **Teal & Yellow** color scheme:
- Teal gradient background (#00bcd4 to #009688)
- Yellow accent buttons (#ffc107)
- Clean white cards with smooth animations

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
