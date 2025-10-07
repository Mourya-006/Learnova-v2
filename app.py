"""
Learnova - AI-Powered Study Buddy
Flask Backend Application
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os
import json
from datetime import datetime
import random
from ai_helper import AIHelper

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

# Initialize AI Helper
print("🔧 Initializing AI Helper...")
ai_helper = AIHelper()

# Data storage
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

def get_user_file(user_id):
    """Get path to user data file"""
    return os.path.join(DATA_DIR, f'user_{user_id}.json')

def load_user_data(user_id):
    """Load user study data"""
    file_path = get_user_file(user_id)
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return {
        'sessions': [],
        'topics_learned': [],
        'quiz_scores': [],
        'total_study_time': 0,
        'streak': 0
    }

def save_user_data(user_id, data):
    """Save user study data"""
    file_path = get_user_file(user_id)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    """Main page"""
    if 'user_id' not in session:
        session['user_id'] = f"user_{random.randint(1000, 9999)}"
    print(f"\n🌐 Index page requested by user: {session['user_id']}")
    print(f"🔍 AI Helper status: use_gemini={ai_helper.use_gemini}")
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat with AI"""
    try:
        data = request.json
        message = data.get('message', '')
        
        print(f"\n📩 Received chat message: '{message}'")
        print(f"🔍 AI Helper use_gemini: {ai_helper.use_gemini}")
        print(f"🔍 AI Helper model: {ai_helper.model}")
        
        response = ai_helper.generate_response(message)
        
        print(f"✅ Response generated: '{response[:100]}...'")
        
        return jsonify({
            'success': True,
            'response': response
        })
    except Exception as e:
        print(f"❌ Chat error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/explain', methods=['POST'])
def explain():
    """Explain a topic"""
    try:
        data = request.json
        topic = data.get('topic', '')
        difficulty = data.get('difficulty', 'intermediate')
        
        print(f"\n📚 Explaining: '{topic}' ({difficulty})")
        
        explanation = ai_helper.explain_topic(topic, difficulty)
        
        return jsonify({
            'success': True,
            'explanation': explanation
        })
    except Exception as e:
        print(f"❌ Explain error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/quiz', methods=['POST'])
def quiz():
    """Generate a quiz"""
    try:
        data = request.json
        topic = data.get('topic', '')
        num_questions = data.get('num_questions', 5)
        difficulty = data.get('difficulty', 'intermediate')
        
        print(f"\n📝 Generating quiz: '{topic}' ({num_questions} questions, {difficulty})")
        
        questions = ai_helper.generate_quiz(topic, num_questions, difficulty)
        
        return jsonify({
            'success': True,
            'quiz': questions
        })
    except Exception as e:
        print(f"❌ Quiz error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/study-tips', methods=['POST'])
def study_tips():
    """Get study tips"""
    try:
        data = request.json
        subject = data.get('subject', '')
        learning_style = data.get('learning_style', 'visual')
        
        print(f"\n💡 Getting study tips: '{subject}' ({learning_style})")
        
        tips = ai_helper.get_study_tips(subject, learning_style)
        
        return jsonify({
            'success': True,
            'tips': tips
        })
    except Exception as e:
        print(f"❌ Study tips error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/session/start', methods=['POST'])
def start_session():
    """Start study session"""
    try:
        user_id = session.get('user_id')
        data = request.json
        
        user_data = load_user_data(user_id)
        session_data = {
            'start_time': datetime.now().isoformat(),
            'topic': data.get('topic', 'General Study'),
            'duration': data.get('duration', 25)
        }
        user_data['sessions'].append(session_data)
        save_user_data(user_id, user_data)
        
        return jsonify({
            'success': True,
            'session_id': len(user_data['sessions']) - 1
        })
    except Exception as e:
        print(f"❌ Start session error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/session/end', methods=['POST'])
def end_session():
    """End study session"""
    try:
        user_id = session.get('user_id')
        data = request.json
        session_id = data.get('session_id')
        
        user_data = load_user_data(user_id)
        if session_id < len(user_data['sessions']):
            user_data['sessions'][session_id]['end_time'] = datetime.now().isoformat()
            user_data['sessions'][session_id]['completed'] = True
            user_data['total_study_time'] += data.get('duration', 25)
            save_user_data(user_id, user_data)
        
        return jsonify({
            'success': True
        })
    except Exception as e:
        print(f"❌ End session error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def stats():
    """Get user statistics"""
    try:
        user_id = session.get('user_id')
        user_data = load_user_data(user_id)
        
        return jsonify({
            'success': True,
            'stats': {
                'total_sessions': len(user_data['sessions']),
                'total_study_time': user_data['total_study_time'],
                'topics_learned': len(user_data['topics_learned']),
                'quizzes_taken': len(user_data['quiz_scores']),
                'streak': user_data['streak']
            }
        })
    except Exception as e:
        print(f"❌ Stats error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Starting Learnova v2.0 - Your AI Study Buddy!")
    print("="*60)
    print(f" Gemini API: {'✅ Enabled' if ai_helper.use_gemini else '⚠️  Disabled (using fallback)'}")
    print("="*60 + "\n")
    
    # Use PORT from environment for deployment platforms like Render
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)
