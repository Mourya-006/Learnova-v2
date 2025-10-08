"""
Learnova - AI-Powered Study Buddy
Flask Backend Application
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import random
from ai_helper import AIHelper
from models import db, User

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///learnova.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this feature.'
login_manager.login_message_category = 'info'

# Initialize Flask-Bcrypt
bcrypt = Bcrypt(app)

# Initialize OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.environ.get('GOOGLE_CLIENT_ID'),
    client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))

# File upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt', 'doc', 'docx'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Initialize AI Helper
print("🔧 Initializing AI Helper...")
ai_helper = AIHelper()

# Data storage
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

# ============================================
# Authentication Routes
# ============================================

@app.route('/login')
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('auth.html', mode='login')

@app.route('/signup')
def signup():
    """Signup page"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('auth.html', mode='signup')

@app.route('/api/auth/signup', methods=['POST'])
def api_signup():
    """Handle email/password signup"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        name = data.get('name', '').strip()
        password = data.get('password', '')
        
        # Validation
        if not email or not name or not password:
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'success': False, 'message': 'Email already registered'}), 400
        
        # Create new user
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            email=email,
            name=name,
            password_hash=password_hash
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Log the user in
        login_user(new_user, remember=True)
        
        return jsonify({
            'success': True,
            'message': 'Account created successfully!',
            'user': new_user.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Signup error: {e}")
        return jsonify({'success': False, 'message': 'An error occurred during signup'}), 500

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """Handle email/password login"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Validation
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password are required'}), 400
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.password_hash:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
        
        # Check password
        if not bcrypt.check_password_hash(user.password_hash, password):
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
        
        # Log the user in
        user.last_login = datetime.utcnow()
        db.session.commit()
        login_user(user, remember=True)
        
        return jsonify({
            'success': True,
            'message': 'Login successful!',
            'user': user.to_dict()
        })
        
    except Exception as e:
        print(f"❌ Login error: {e}")
        return jsonify({'success': False, 'message': 'An error occurred during login'}), 500

@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    """Handle logout"""
    if current_user.is_authenticated:
        logout_user()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/auth/user')
def api_get_user():
    """Get current user info"""
    if current_user.is_authenticated:
        return jsonify({
            'success': True,
            'authenticated': True,
            'user': current_user.to_dict()
        })
    else:
        return jsonify({
            'success': True,
            'authenticated': False,
            'user': None
        })

@app.route('/auth/google')
def google_login():
    """Initiate Google OAuth login"""
    redirect_uri = url_for('google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/google/callback')
def google_callback():
    """Handle Google OAuth callback"""
    try:
        token = google.authorize_access_token()
        user_info = token.get('userinfo')
        
        if not user_info:
            flash('Failed to get user info from Google', 'error')
            return redirect(url_for('login'))
        
        email = user_info.get('email')
        name = user_info.get('name')
        google_id = user_info.get('sub')
        profile_picture = user_info.get('picture')
        
        # Check if user exists
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Update Google ID and profile picture if not set
            if not user.google_id:
                user.google_id = google_id
            if not user.profile_picture:
                user.profile_picture = profile_picture
            user.last_login = datetime.utcnow()
        else:
            # Create new user
            user = User(
                email=email,
                name=name,
                google_id=google_id,
                profile_picture=profile_picture
            )
            db.session.add(user)
        
        db.session.commit()
        login_user(user, remember=True)
        
        flash('Successfully logged in with Google!', 'success')
        return redirect(url_for('index'))
        
    except Exception as e:
        print(f"❌ Google OAuth error: {e}")
        flash('An error occurred during Google login', 'error')
        return redirect(url_for('login'))

# ============================================
# Main Application Routes
# ============================================

@app.route('/test')
def test():
    """Test route to verify server is working"""
    return f"""
    <html>
    <body style="background: #000; color: #0f0; font-family: monospace; padding: 50px;">
        <h1>✅ Server is Working!</h1>
        <p>If you see this, the Flask server is running correctly.</p>
        <p>Authenticated: {current_user.is_authenticated}</p>
        <p><a href="/" style="color: #ff9800;">Click here to go to main page</a></p>
    </body>
    </html>
    """

@app.route('/')
def index():
    """Main page - accessible to everyone (guest or logged in)"""
    if current_user.is_authenticated:
        print(f"\n🌐 Index page requested by authenticated user: {current_user.email}")
    else:
        # Guest mode
        if 'guest_id' not in session:
            session['guest_id'] = f"guest_{random.randint(10000, 99999)}"
        print(f"\n🌐 Index page requested by guest: {session['guest_id']}")
    
    print(f"🔍 AI Helper status: use_gemini={ai_helper.use_gemini}")
    print(f"✅ Rendering index.html for {'authenticated user' if current_user.is_authenticated else 'guest'}")
    return render_template('index.html', user=current_user if current_user.is_authenticated else None)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat with AI - accessible to everyone"""
    try:
        # Handle both JSON and FormData
        if request.is_json:
            message = request.json.get('message', '')
            file_path = None
        else:
            message = request.form.get('message', '')
            file_path = None
            
            # Handle file upload
            if 'file' in request.files:
                file = request.files['file']
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    unique_filename = f"{timestamp}_{filename}"
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                    file.save(file_path)
                    print(f"📎 File uploaded: {file_path}")
        
        print(f"\n📩 Received chat message: '{message}'")
        print(f"� File path: {file_path}")
        print(f"�🔍 AI Helper use_gemini: {ai_helper.use_gemini}")
        
        # Generate response with file context if available
        if file_path:
            response = ai_helper.generate_response_with_file(message, file_path)
            # Clean up uploaded file after processing
            try:
                os.remove(file_path)
                print(f"🗑️ Cleaned up file: {file_path}")
            except:
                pass
        else:
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
    # Create database tables
    with app.app_context():
        db.create_all()
        print("✅ Database initialized")
    
    # Print all registered routes for debugging
    print("\n📋 Registered Routes:")
    for rule in app.url_map.iter_rules():
        print(f"   {rule.endpoint:30} {rule.rule}")
    
    print("\n" + "="*60)
    print("🚀 Starting Learnova v2.0 - Your AI Study Buddy!")
    print("="*60)
    print(f" Gemini API: {'✅ Enabled' if ai_helper.use_gemini else '⚠️  Disabled (using fallback)'}")
    print(f" Authentication: ✅ Enabled")
    print("="*60 + "\n")
    
    # Use PORT from environment for deployment platforms like Render
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)
