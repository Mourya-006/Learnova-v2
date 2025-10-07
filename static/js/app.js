// Learnova - Frontend JavaScript

// State
let timerInterval = null;
let timerSeconds = 25 * 60;
let timerRunning = false;
let currentSessionId = null;
let quizData = null;
let userAnswers = {};

// DOM Elements
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const chatMessages = document.getElementById('chatMessages');
const timerDisplay = document.getElementById('timerDisplay');
const startTimerBtn = document.getElementById('startTimer');
const pauseTimerBtn = document.getElementById('pauseTimer');
const resetTimerBtn = document.getElementById('resetTimer');
const presetBtns = document.querySelectorAll('.preset-btn');
const loadingSpinner = document.getElementById('loadingSpinner');
const quizModal = document.getElementById('quizModal');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    updateTimerDisplay();
});

// Event Listeners
function setupEventListeners() {
    // Chat
    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    // Timer
    startTimerBtn.addEventListener('click', startTimer);
    pauseTimerBtn.addEventListener('click', pauseTimer);
    resetTimerBtn.addEventListener('click', resetTimer);
    
    presetBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const minutes = parseInt(btn.dataset.minutes);
            setTimerPreset(minutes);
        });
    });

    // Custom time input
    document.getElementById('setCustomTime').addEventListener('click', setCustomTime);
    document.getElementById('customMinutes').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') setCustomTime();
    });

    // Features
    document.getElementById('explainBtn').addEventListener('click', explainTopic);
    document.getElementById('generateQuizBtn').addEventListener('click', generateQuiz);
    document.getElementById('getTipsBtn').addEventListener('click', getStudyTips);
    document.getElementById('closeQuiz').addEventListener('click', closeQuizModal);
}

// Chat Functions
async function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;

    // Add user message
    addMessage(message, 'user');
    chatInput.value = '';

    // Show loading
    showLoading();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        hideLoading();

        if (data.success) {
            addMessage(data.response, 'bot');
        } else {
            addMessage('Sorry, I encountered an error. Please try again!', 'bot');
        }
    } catch (error) {
        hideLoading();
        console.error('Chat error:', error);
        addMessage('Connection error. Please check your connection and try again.', 'bot');
    }
}

function addMessage(text, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const icon = document.createElement('i');
    icon.className = `fas ${type === 'user' ? 'fa-user' : 'fa-robot'} message-icon`;
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    // Convert line breaks and format text
    const formattedText = text.split('\n').map(line => {
        if (line.startsWith('• ')) {
            return `<p>${line}</p>`;
        }
        return line ? `<p>${line}</p>` : '<br>';
    }).join('');
    
    content.innerHTML = formattedText;
    
    messageDiv.appendChild(icon);
    messageDiv.appendChild(content);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Timer Functions
function updateTimerDisplay() {
    const minutes = Math.floor(timerSeconds / 60);
    const seconds = timerSeconds % 60;
    timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

function startTimer() {
    if (timerRunning) return;
    
    timerRunning = true;
    startTimerBtn.disabled = true;
    pauseTimerBtn.disabled = false;
    
    // Start session
    startSession();
    
    timerInterval = setInterval(() => {
        timerSeconds--;
        updateTimerDisplay();
        
        if (timerSeconds <= 0) {
            pauseTimer();
            endSession();
            showNotification('⏰ Timer completed! Great job!');
        }
    }, 1000);
}

function pauseTimer() {
    timerRunning = false;
    clearInterval(timerInterval);
    startTimerBtn.disabled = false;
    pauseTimerBtn.disabled = true;
}

function resetTimer() {
    pauseTimer();
    
    // Get active preset or default to 25 minutes
    const activePreset = document.querySelector('.preset-btn.active');
    const minutes = activePreset ? parseInt(activePreset.dataset.minutes) : 25;
    timerSeconds = minutes * 60;
    
    updateTimerDisplay();
    
    if (currentSessionId !== null) {
        endSession();
    }
}

function setTimerPreset(minutes) {
    if (timerRunning) return;
    
    // Update active button
    presetBtns.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Set timer
    timerSeconds = minutes * 60;
    updateTimerDisplay();
    
    // Clear custom input
    document.getElementById('customMinutes').value = '';
}

function setCustomTime() {
    if (timerRunning) {
        showNotification('⚠️ Stop the timer first!');
        return;
    }
    
    const customInput = document.getElementById('customMinutes');
    const minutes = parseInt(customInput.value);
    
    if (!minutes || minutes < 1 || minutes > 180) {
        showNotification('⚠️ Please enter a valid time (1-180 minutes)');
        return;
    }
    
    // Remove active from presets
    presetBtns.forEach(btn => btn.classList.remove('active'));
    
    // Set timer
    timerSeconds = minutes * 60;
    updateTimerDisplay();
    
    // Clear input
    customInput.value = '';
    
    showNotification(`✅ Timer set to ${minutes} minutes!`);
}


// Session Management
async function startSession() {
    try {
        const response = await fetch('/api/session/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                topic: 'Study Session',
                duration: Math.floor(timerSeconds / 60)
            })
        });
        
        const data = await response.json();
        if (data.success) {
            currentSessionId = data.session_id;
        }
    } catch (error) {
        console.error('Session start error:', error);
    }
}

async function endSession() {
    if (currentSessionId === null) return;
    
    try {
        await fetch('/api/session/end', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: currentSessionId,
                duration: Math.floor(timerSeconds / 60)
            })
        });
        
        currentSessionId = null;
    } catch (error) {
        console.error('Session end error:', error);
    }
}

// Explain Topic
async function explainTopic() {
    const topic = document.getElementById('topicInput').value.trim();
    const difficulty = document.getElementById('difficultySelect').value;
    
    if (!topic) {
        showNotification('⚠️ Please enter a topic!');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/api/explain', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic, difficulty })
        });
        
        const data = await response.json();
        hideLoading();
        
        if (data.success) {
            addMessage(`📚 Explanation of "${topic}" (${difficulty} level):\n\n${data.explanation}`, 'bot');
            document.getElementById('topicInput').value = '';
        } else {
            showNotification('❌ Failed to explain topic');
        }
    } catch (error) {
        hideLoading();
        console.error('Explain error:', error);
        showNotification('❌ Connection error');
    }
}

// Generate Quiz
async function generateQuiz() {
    const topic = document.getElementById('quizTopic').value.trim();
    const numQuestions = parseInt(document.getElementById('numQuestions').value);
    const difficulty = document.getElementById('quizDifficulty').value;
    
    if (!topic) {
        showNotification('⚠️ Please enter a quiz topic!');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/api/quiz', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic, num_questions: numQuestions, difficulty })
        });
        
        const data = await response.json();
        hideLoading();
        
        if (data.success) {
            quizData = data.quiz;
            userAnswers = {};
            displayQuiz();
            document.getElementById('quizTopic').value = '';
        } else {
            showNotification('❌ Failed to generate quiz');
        }
    } catch (error) {
        hideLoading();
        console.error('Quiz error:', error);
        showNotification('❌ Connection error');
    }
}

function displayQuiz() {
    const quizContent = document.getElementById('quizContent');
    quizContent.innerHTML = '';
    
    quizData.forEach((q, index) => {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'quiz-question';
        questionDiv.innerHTML = `
            <div class="question-number">Question ${index + 1}</div>
            <div class="question-text">${q.question}</div>
            <div class="quiz-options-list">
                ${q.options.map((option, optIndex) => `
                    <div class="quiz-option" data-question="${index}" data-answer="${option.charAt(0)}">
                        ${option}
                    </div>
                `).join('')}
            </div>
        `;
        quizContent.appendChild(questionDiv);
    });
    
    // Add submit button
    const submitBtn = document.createElement('button');
    submitBtn.className = 'quiz-submit';
    submitBtn.textContent = '✓ Submit Quiz';
    submitBtn.onclick = submitQuiz;
    quizContent.appendChild(submitBtn);
    
    // Add option click handlers
    document.querySelectorAll('.quiz-option').forEach(option => {
        option.addEventListener('click', function() {
            const questionIndex = this.dataset.question;
            const answer = this.dataset.answer;
            
            // Remove selected from siblings
            this.parentElement.querySelectorAll('.quiz-option').forEach(opt => {
                opt.classList.remove('selected');
            });
            
            // Add selected to clicked
            this.classList.add('selected');
            userAnswers[questionIndex] = answer;
        });
    });
    
    quizModal.classList.add('active');
}

function submitQuiz() {
    let score = 0;
    
    quizData.forEach((q, index) => {
        const userAnswer = userAnswers[index];
        const correctAnswer = q.correct_answer;
        const questionDiv = document.querySelectorAll('.quiz-question')[index];
        
        // Mark options
        const options = questionDiv.querySelectorAll('.quiz-option');
        options.forEach(option => {
            const answer = option.dataset.answer;
            if (answer === correctAnswer) {
                option.classList.add('correct');
            } else if (answer === userAnswer && answer !== correctAnswer) {
                option.classList.add('incorrect');
            }
        });
        
        // Add explanation
        const explanationDiv = document.createElement('div');
        explanationDiv.className = 'explanation';
        explanationDiv.innerHTML = `<strong>Explanation:</strong> ${q.explanation}`;
        questionDiv.appendChild(explanationDiv);
        
        if (userAnswer === correctAnswer) {
            score++;
        }
    });
    
    // Show score
    const scoreDiv = document.createElement('div');
    scoreDiv.className = 'quiz-question';
    scoreDiv.innerHTML = `
        <h3 style="text-align: center; color: #009688; font-size: 1.8rem;">
            🎯 Score: ${score}/${quizData.length}
        </h3>
        <p style="text-align: center; margin-top: 10px;">
            ${score === quizData.length ? 'Perfect score! 🌟' : 
              score >= quizData.length * 0.7 ? 'Great job! 👏' : 
              'Keep practicing! 💪'}
        </p>
    `;
    document.getElementById('quizContent').insertBefore(
        scoreDiv,
        document.getElementById('quizContent').firstChild
    );
    
    // Remove submit button
    document.querySelector('.quiz-submit').remove();
}

function closeQuizModal() {
    quizModal.classList.remove('active');
}

// Study Tips
async function getStudyTips() {
    const subject = document.getElementById('studySubject').value.trim();
    const learningStyle = document.getElementById('learningStyle').value;
    
    if (!subject) {
        showNotification('⚠️ Please enter a subject!');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/api/study-tips', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ subject, learning_style: learningStyle })
        });
        
        const data = await response.json();
        hideLoading();
        
        if (data.success) {
            addMessage(`💡 Study tips for ${subject} (${learningStyle} learner):\n\n${data.tips}`, 'bot');
            document.getElementById('studySubject').value = '';
        } else {
            showNotification('❌ Failed to get study tips');
        }
    } catch (error) {
        hideLoading();
        console.error('Tips error:', error);
        showNotification('❌ Connection error');
    }
}

// UI Helpers
function showLoading() {
    loadingSpinner.classList.add('active');
}

function hideLoading() {
    loadingSpinner.classList.remove('active');
}

function showNotification(message) {
    addMessage(message, 'bot');
}

// Stats Functions
async function showStats() {
    showLoading();
    
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        hideLoading();
        
        if (data.success) {
            displayStats(data.stats);
            document.getElementById('statsModal').classList.add('active');
        } else {
            showNotification('❌ Failed to load stats');
        }
    } catch (error) {
        hideLoading();
        console.error('Stats error:', error);
        showNotification('❌ Connection error');
    }
}

function displayStats(stats) {
    const statsContent = document.getElementById('statsContent');
    statsContent.innerHTML = `
        <div class="stat-card">
            <i class="fas fa-clock stat-icon"></i>
            <div class="stat-info">
                <h3>Total Study Time</h3>
                <div class="stat-value">${stats.total_study_time}</div>
                <div class="stat-label">minutes</div>
            </div>
        </div>
        
        <div class="stat-card">
            <i class="fas fa-book-reader stat-icon"></i>
            <div class="stat-info">
                <h3>Study Sessions</h3>
                <div class="stat-value">${stats.total_sessions}</div>
                <div class="stat-label">completed</div>
            </div>
        </div>
        
        <div class="stat-card">
            <i class="fas fa-graduation-cap stat-icon"></i>
            <div class="stat-info">
                <h3>Topics Learned</h3>
                <div class="stat-value">${stats.topics_learned}</div>
                <div class="stat-label">topics</div>
            </div>
        </div>
        
        <div class="stat-card">
            <i class="fas fa-clipboard-check stat-icon"></i>
            <div class="stat-info">
                <h3>Quizzes Taken</h3>
                <div class="stat-value">${stats.quizzes_taken}</div>
                <div class="stat-label">quizzes</div>
            </div>
        </div>
        
        <div class="stat-card">
            <i class="fas fa-fire stat-icon"></i>
            <div class="stat-info">
                <h3>Current Streak</h3>
                <div class="stat-value">${stats.streak}</div>
                <div class="stat-label">days</div>
            </div>
        </div>
    `;
}

function closeStatsModal() {
    document.getElementById('statsModal').classList.remove('active');
}

