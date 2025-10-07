import streamlit as st
import os
from datetime import datetime
import json
from pathlib import Path
from ai_helper import AIHelper

# Page configuration
st.set_page_config(
    page_title="Learnova - AI Study Buddy",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for teal/yellow theme
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #00bcd4;
        --secondary-color: #ffc107;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #00bcd4 0%, #009688 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: white;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #ffc107;
    }
    
    .feature-card h3 {
        color: #00bcd4;
        margin-top: 0;
    }
    
    /* Chat messages */
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    
    .chat-message.user {
        background-color: #e1f5fe;
        border-left: 4px solid #00bcd4;
    }
    
    .chat-message.assistant {
        background-color: #fff9c4;
        border-left: 4px solid #ffc107;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #ffc107;
        color: #000;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #ffb300;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Timer display */
    .timer-display {
        font-size: 3rem;
        font-weight: bold;
        color: #00bcd4;
        text-align: center;
        padding: 2rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Stats card */
    .stat-card {
        background: linear-gradient(135deg, #00bcd4 0%, #009688 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stat-card h3 {
        margin: 0;
        font-size: 2rem;
    }
    
    .stat-card p {
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
    }
    
    /* Quiz styling */
    .quiz-question {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .quiz-question h4 {
        color: #00bcd4;
    }
</style>
""", unsafe_allow_html=True)

# Initialize AI Helper
@st.cache_resource
def init_ai_helper():
    return AIHelper()

ai_helper = init_ai_helper()

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_quiz' not in st.session_state:
    st.session_state.current_quiz = None
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'total_study_time': 0,
        'sessions_completed': 0,
        'topics_learned': 0,
        'quizzes_taken': 0,
        'current_streak': 0
    }
if 'timer_seconds' not in st.session_state:
    st.session_state.timer_seconds = 1500  # 25 minutes default
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False

# Header
st.markdown("""
<div class="main-header">
    <h1>🎓 Learnova</h1>
    <p>Your AI-Powered Study Companion</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for navigation
with st.sidebar:
    st.markdown("### 📚 Features")
    page = st.radio(
        "Choose a feature:",
        ["💬 Chat", "📖 Explain Topic", "📝 Generate Quiz", "⏰ Study Timer", "💡 Study Tips", "📊 My Progress"]
    )
    
    st.markdown("---")
    st.markdown("### 🎨 About")
    st.info("Learnova helps you study smarter with AI-powered explanations, quizzes, and personalized tips!")

# Main content based on selected page
if page == "💬 Chat":
    st.markdown("### 💬 Chat with Learnova")
    st.markdown("Ask me anything about your studies!")
    
    # Display chat history
    for message in st.session_state.chat_history:
        role = message['role']
        content = message['content']
        if role == 'user':
            st.markdown(f'<div class="chat-message user"><strong>You:</strong><br>{content}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message assistant"><strong>Learnova:</strong><br>{content}</div>', unsafe_allow_html=True)
    
    # Chat input
    user_message = st.text_input("Type your message:", key="chat_input")
    if st.button("Send", key="send_chat"):
        if user_message:
            # Add user message
            st.session_state.chat_history.append({'role': 'user', 'content': user_message})
            
            # Get AI response
            with st.spinner("Thinking..."):
                response = ai_helper.generate_response(user_message)
            
            # Add AI response
            st.session_state.chat_history.append({'role': 'assistant', 'content': response})
            st.rerun()

elif page == "📖 Explain Topic":
    st.markdown("### 📖 Explain a Topic")
    
    topic = st.text_input("Enter a topic you want to learn:", key="explain_topic_input")
    difficulty = st.selectbox("Select difficulty level:", ["beginner", "intermediate", "advanced"])
    
    if st.button("Get Explanation", key="explain_button"):
        if topic:
            with st.spinner("Generating explanation..."):
                explanation = ai_helper.explain_topic(topic, difficulty)
            
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.markdown(f"**{topic.title()}** ({difficulty.capitalize()} Level)")
            st.markdown(explanation)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Update stats
            st.session_state.user_data['topics_learned'] += 1
        else:
            st.warning("Please enter a topic!")

elif page == "📝 Generate Quiz":
    st.markdown("### 📝 Generate a Quiz")
    
    if st.session_state.current_quiz is None:
        quiz_topic = st.text_input("Enter quiz topic:", key="quiz_topic_input")
        num_questions = st.slider("Number of questions:", 3, 10, 5)
        quiz_difficulty = st.selectbox("Difficulty:", ["beginner", "intermediate", "advanced"], key="quiz_difficulty")
        
        if st.button("Generate Quiz", key="generate_quiz_button"):
            if quiz_topic:
                with st.spinner("Creating your quiz..."):
                    quiz_data = ai_helper.generate_quiz(quiz_topic, num_questions, quiz_difficulty)
                
                if quiz_data and 'questions' in quiz_data:
                    st.session_state.current_quiz = quiz_data
                    st.session_state.quiz_answers = {}
                    st.rerun()
                else:
                    st.error("Failed to generate quiz. Please try again.")
            else:
                st.warning("Please enter a quiz topic!")
    else:
        # Display quiz
        quiz = st.session_state.current_quiz
        st.markdown(f"**Quiz Topic:** {quiz.get('topic', 'Unknown')}")
        st.markdown(f"**Difficulty:** {quiz.get('difficulty', 'Unknown')}")
        st.markdown("---")
        
        # Questions
        for i, question in enumerate(quiz['questions']):
            st.markdown(f'<div class="quiz-question">', unsafe_allow_html=True)
            st.markdown(f"**Question {i+1}:** {question['question']}")
            
            # Radio buttons for options
            answer = st.radio(
                "Select your answer:",
                question['options'],
                key=f"q_{i}",
                index=None
            )
            
            if answer:
                st.session_state.quiz_answers[i] = answer
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Submit quiz
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Submit Quiz", key="submit_quiz"):
                if len(st.session_state.quiz_answers) == len(quiz['questions']):
                    correct = 0
                    for i, question in enumerate(quiz['questions']):
                        if st.session_state.quiz_answers.get(i) == question['correct_answer']:
                            correct += 1
                    
                    score = (correct / len(quiz['questions'])) * 100
                    st.success(f"Quiz Complete! Your score: {score:.1f}% ({correct}/{len(quiz['questions'])})")
                    
                    # Update stats
                    st.session_state.user_data['quizzes_taken'] += 1
                else:
                    st.warning("Please answer all questions!")
        
        with col2:
            if st.button("New Quiz", key="new_quiz"):
                st.session_state.current_quiz = None
                st.session_state.quiz_answers = {}
                st.rerun()

elif page == "⏰ Study Timer":
    st.markdown("### ⏰ Study Timer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Timer display
        minutes = st.session_state.timer_seconds // 60
        seconds = st.session_state.timer_seconds % 60
        st.markdown(f'<div class="timer-display">{minutes:02d}:{seconds:02d}</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Quick Presets")
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("15 min", key="preset_15"):
                st.session_state.timer_seconds = 900
                st.session_state.timer_running = False
                st.rerun()
        
        with col_b:
            if st.button("25 min", key="preset_25"):
                st.session_state.timer_seconds = 1500
                st.session_state.timer_running = False
                st.rerun()
        
        with col_c:
            if st.button("45 min", key="preset_45"):
                st.session_state.timer_seconds = 2700
                st.session_state.timer_running = False
                st.rerun()
        
        st.markdown("### Custom Time")
        custom_minutes = st.number_input("Minutes:", min_value=1, max_value=180, value=25, key="custom_timer")
        if st.button("Set Custom Time", key="set_custom"):
            st.session_state.timer_seconds = custom_minutes * 60
            st.session_state.timer_running = False
            st.rerun()
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("▶️ Start" if not st.session_state.timer_running else "⏸️ Pause", key="start_pause"):
            st.session_state.timer_running = not st.session_state.timer_running
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset", key="reset_timer"):
            st.session_state.timer_seconds = 1500
            st.session_state.timer_running = False
            st.rerun()
    
    with col3:
        if st.button("✅ End Session", key="end_session"):
            # Update stats
            st.session_state.user_data['sessions_completed'] += 1
            study_time = (1500 - st.session_state.timer_seconds) // 60
            st.session_state.user_data['total_study_time'] += study_time
            
            st.success(f"Session complete! You studied for {study_time} minutes.")
            st.session_state.timer_seconds = 1500
            st.session_state.timer_running = False
    
    # Timer countdown logic
    if st.session_state.timer_running and st.session_state.timer_seconds > 0:
        import time
        time.sleep(1)
        st.session_state.timer_seconds -= 1
        if st.session_state.timer_seconds == 0:
            st.session_state.timer_running = False
            st.balloons()
            st.success("⏰ Time's up! Great study session!")
        st.rerun()

elif page == "💡 Study Tips":
    st.markdown("### 💡 Get Personalized Study Tips")
    
    subject = st.text_input("What subject are you studying?", key="tips_subject")
    learning_style = st.selectbox(
        "Your learning style:",
        ["visual", "auditory", "kinesthetic", "reading/writing"],
        key="learning_style"
    )
    
    if st.button("Get Study Tips", key="get_tips_button"):
        if subject:
            with st.spinner("Generating personalized tips..."):
                tips = ai_helper.get_study_tips(subject, learning_style)
            
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.markdown(f"**Study Tips for {subject.title()}**")
            st.markdown(f"*Tailored for {learning_style} learners*")
            st.markdown(tips)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Please enter a subject!")

elif page == "📊 My Progress":
    st.markdown("### 📊 Your Learning Progress")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h3>{st.session_state.user_data['total_study_time']}</h3>
            <p>Minutes Studied</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h3>{st.session_state.user_data['sessions_completed']}</h3>
            <p>Sessions Completed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <h3>{st.session_state.user_data['topics_learned']}</h3>
            <p>Topics Learned</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col4, col5 = st.columns(2)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <h3>{st.session_state.user_data['quizzes_taken']}</h3>
            <p>Quizzes Taken</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="stat-card">
            <h3>{st.session_state.user_data['current_streak']}</h3>
            <p>Day Streak 🔥</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🎯 Keep up the great work!")
    st.info("Continue learning to improve your stats and maintain your streak!")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "Made with ❤️ using Streamlit & Google Gemini AI"
    "</div>",
    unsafe_allow_html=True
)
