"""
AI Helper for Learnova
Handles all AI-powered features using Google Gemini API
"""

import os
import json

class AIHelper:
    """AI Helper using Google Gemini API"""
    
    def __init__(self):
        """Initialize AI Helper with Gemini"""
        self.use_gemini = False
        self.model = None
        
        # Get API key - check Streamlit secrets first, then environment variable
        api_key = None
        
        # Try Streamlit secrets first (for cloud deployment)
        try:
            import streamlit as st
            if hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets:
                api_key = st.secrets['GEMINI_API_KEY']
                print("✅ Found GEMINI_API_KEY in Streamlit secrets")
        except:
            pass
        
        # Fall back to environment variable (for local development)
        if not api_key:
            api_key = os.environ.get('GEMINI_API_KEY')
            if api_key:
                print(f"✅ Found GEMINI_API_KEY in environment: {api_key[:20]}...")
        
        if not api_key:
            print("⚠️  WARNING: GEMINI_API_KEY not set!")
            print("   For local: Set environment variable")
            print("   For Streamlit Cloud: Add to Secrets in settings")
            return
        
        # Try to import and configure Gemini
        try:
            from google import genai
            
            # Configure API (new google-genai SDK)
            self.client = genai.Client(api_key=api_key)
            
            # Model name for Gemini 2.5 Flash
            self.model_name = 'gemini-2.5-flash'
            self.model = self.client  # keep self.model truthy for use_gemini checks
            self.use_gemini = True
            
            print("✅ Gemini AI successfully initialized with gemini-2.5-flash!")
            print(f"🔍 use_gemini flag set to: {self.use_gemini}")
            print(f"🔍 client object: {self.client}")
                
        except ImportError:
            print("❌ ERROR: google-genai package not installed")
            print("   Install with: pip install google-genai")
            self.use_gemini = False
        except Exception as e:
            print(f"❌ ERROR initializing Gemini: {e}")
            import traceback
            traceback.print_exc()
            self.use_gemini = False
    
    def generate_response(self, message, context=None):
        """Generate AI response to user message"""
        print(f"\n🤖 generate_response called")
        print(f"   Message: '{message[:100]}'")
        print(f"   use_gemini: {self.use_gemini}")
        print(f"   model exists: {self.model is not None}")
        
        if not self.use_gemini or not self.model:
            print("   ➡️  Using fallback")
            return self._fallback_response()
        
        try:
            print("   ➡️  Calling Gemini API...")
            
            prompt = f"""You are Learnova, a friendly AI study buddy. Help students learn effectively.

Be:
- Encouraging and supportive
- Clear and concise
- Educational and helpful
- Use emojis occasionally 📚✨

Student message: {message}

Your response:"""
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            result = response.text
            
            print(f"   ✅ Gemini responded: '{result[:100]}...'")
            return result
            
        except Exception as e:
            print(f"   ❌ Gemini error: {e}")
            import traceback
            traceback.print_exc()
            return self._fallback_response()
    
    def generate_response_with_file(self, message, file_path):
        """Generate AI response with file/image context"""
        print(f"\n🤖 generate_response_with_file called")
        print(f"   Message: '{message[:100]}'")
        print(f"   File: {file_path}")
        print(f"   use_gemini: {self.use_gemini}")
        
        if not self.use_gemini or not self.model:
            return self._fallback_file_response()
        
        try:
            from google import genai
            from PIL import Image
            
            file_ext = file_path.rsplit('.', 1)[1].lower()
            
            # Handle images
            if file_ext in ['png', 'jpg', 'jpeg', 'gif']:
                print("   📷 Processing image...")
                image = Image.open(file_path)
                
                if message:
                    prompt = f"""You are Learnova, a helpful AI study buddy. Analyze this image and answer the student's question.

Student question: {message}

Provide a clear, educational response based on the image content."""
                else:
                    prompt = "Analyze this image and explain what you see. Help the student understand the content."
                
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=[prompt, image]
                )
                return response.text
            
            # Handle text files
            elif file_ext in ['txt', 'pdf']:
                print("   📄 Processing text file...")
                
                # Read text content
                if file_ext == 'txt':
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                else:
                    # For PDF, we'll need PyPDF2 or similar
                    try:
                        import PyPDF2
                        with open(file_path, 'rb') as f:
                            pdf_reader = PyPDF2.PdfReader(f)
                            content = ""
                            for page in pdf_reader.pages[:5]:  # First 5 pages only
                                content += page.extract_text()
                    except:
                        return "I can see you uploaded a PDF, but I need the PyPDF2 library to read it. For now, please try uploading images or text files! 📄"
                
                prompt = f"""You are Learnova, a helpful AI study buddy. The student has uploaded a document with the following content:

--- Document Content ---
{content[:3000]}  
---

Student's question: {message if message else "Please explain and summarize this document"}

Provide a helpful, educational response."""
                
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                return response.text
            
            else:
                return "Sorry, I can only process images (PNG, JPG, JPEG, GIF) and text files (TXT, PDF) at the moment. 📎"
                
        except Exception as e:
            print(f"   ❌ File processing error: {e}")
            import traceback
            traceback.print_exc()
            return self._fallback_file_response()
    
    def explain_topic(self, topic, difficulty='intermediate'):
        """Explain a topic"""
        print(f"\n📚 explain_topic: '{topic}' ({difficulty})")
        
        if not self.use_gemini or not self.model:
            return self._fallback_explain(topic)
        
        try:
            difficulty_guides = {
                'beginner': 'Explain in very simple terms for a complete beginner. Use everyday analogies.',
                'intermediate': 'Explain clearly with examples, assuming basic knowledge.',
                'advanced': 'Provide detailed explanation with technical depth.'
            }
            
            prompt = f"""Explain the topic: {topic}

Level: {difficulty}
{difficulty_guides.get(difficulty, difficulty_guides['intermediate'])}

Include:
1. Clear definition
2. Key concepts
3. Real-world examples
4. Why it matters

Keep it engaging and educational!"""
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
            
        except Exception as e:
            print(f"❌ Explain error: {e}")
            return self._fallback_explain(topic)
    
    def generate_quiz(self, topic, num_questions=5, difficulty='intermediate'):
        """Generate quiz questions"""
        print(f"\n📝 generate_quiz: '{topic}' ({num_questions} questions, {difficulty})")
        
        if not self.use_gemini or not self.model:
            return self._fallback_quiz(topic, num_questions)
        
        try:
            prompt = f"""Create {num_questions} multiple choice questions about: {topic}
Difficulty: {difficulty}

Return ONLY valid JSON array (no markdown, no explanations):
[
  {{
    "question": "Question text?",
    "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
    "correct_answer": "A",
    "explanation": "Why this is correct"
  }}
]

Make questions progressively challenging."""
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            content = response.text.strip()
            
            # Remove markdown code blocks
            if '```' in content:
                start = content.find('[')
                end = content.rfind(']') + 1
                if start >= 0 and end > start:
                    content = content[start:end]
            
            quiz = json.loads(content)
            print(f"✅ Generated {len(quiz)} questions")
            return quiz
            
        except Exception as e:
            print(f"❌ Quiz generation error: {e}")
            import traceback
            traceback.print_exc()
            return self._fallback_quiz(topic, num_questions)
    
    def get_study_tips(self, subject, learning_style='visual'):
        """Get study tips"""
        print(f"\n💡 get_study_tips: '{subject}' ({learning_style})")
        
        if not self.use_gemini or not self.model:
            return self._fallback_tips(subject, learning_style)
        
        try:
            prompt = f"""Provide practical study tips for: {subject}
Learning style: {learning_style}

Include:
- Specific strategies for {learning_style} learners
- Effective techniques for {subject}
- Time management tips
- Resource recommendations
- Practice methods

Be actionable and encouraging!"""
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
            
        except Exception as e:
            print(f"❌ Study tips error: {e}")
            return self._fallback_tips(subject, learning_style)
    
    # Fallback methods
    
    def _fallback_response(self):
        """Fallback chat response"""
        return """Hi! I'm Learnova, your study buddy! 📚

I can help you with:
• 📖 Explaining topics clearly
• 📝 Creating practice quizzes  
• 💡 Providing study tips
• ⏱️ Tracking study sessions
• 🎯 Keeping you motivated

Try the buttons on the right to explore different features!

⚠️ Note: AI features require Gemini API key to be set."""
    
    def _fallback_file_response(self):
        """Fallback file processing response"""
        return """📎 **File Upload Feature**

I can see you've uploaded a file! However, to analyze files and images, I need the Gemini API key to be configured.

**What I can do with files:**
• 📷 Analyze images and diagrams
• 📄 Read and summarize text documents
• 🤔 Answer questions about uploaded content

**To enable this feature:**
Set up your Gemini API key in the environment variables or Streamlit secrets.

⚠️ Currently using fallback mode."""
    
    def _fallback_explain(self, topic):
        """Fallback explanation"""
        return f"""📚 **About: {topic}**

To get AI-powered explanations, please set up your Gemini API key:

**Setup Steps:**
1. Visit: https://makersuite.google.com/app/apikey
2. Create a free API key
3. Set environment variable:
   ```
   $env:GEMINI_API_KEY="your-key-here"
   ```
4. Restart Learnova

**In the meantime:**
• Search for "{topic}" on educational websites
• Watch video tutorials
• Try the study timer and quiz features!"""
    
    def _fallback_quiz(self, topic, num_questions):
        """Fallback quiz"""
        questions = []
        for i in range(num_questions):
            questions.append({
                "question": f"Demo question {i+1} about {topic}",
                "options": [
                    "A) This is a sample quiz",
                    "B) Set up Gemini API for real quizzes",
                    "C) Get your API key from Google AI Studio",
                    "D) All of the above"
                ],
                "correct_answer": "D",
                "explanation": "Set up your Gemini API key to get AI-generated quizzes on any topic!"
            })
        return questions
    
    def _fallback_tips(self, subject, learning_style):
        """Fallback study tips"""
        return f"""💡 **Study Tips for {subject}**

**General Strategies:**
✅ Break down into smaller topics
⏰ Use Pomodoro Technique (25 min focus)
📝 Practice active recall
🎯 Set specific goals
📊 Track your progress
🤝 Teach concepts to others

**For {learning_style} learners:**
{'📺 Use diagrams, videos, and visual aids' if learning_style == 'visual' else ''}
{'🎧 Use audio resources and discussions' if learning_style == 'auditory' else ''}
{'🔨 Practice hands-on exercises' if learning_style == 'kinesthetic' else ''}

💪 Stay consistent and use the study timer!

⚠️ For personalized AI tips, set up your Gemini API key."""
