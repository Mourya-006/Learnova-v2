// Learnova - Frontend JavaScript - World's Best Study App

// State
let timerInterval = null;
let timerSeconds = 25 * 60;
let timerRunning = false;
let currentSessionId = null;
let quizData = null;
let userAnswers = {};
let uploadedFile = null;

// ============================================
// RIPPLE EFFECT FOR BUTTONS
// ============================================
function createRipple(event) {
    const button = event.currentTarget;
    const ripple = document.createElement('span');
    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    ripple.classList.add('ripple');
    
    button.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// Add ripple effect to all buttons
function initializeRippleEffects() {
    const buttons = document.querySelectorAll('button, .btn-primary, .btn-secondary, .quick-action');
    buttons.forEach(button => {
        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        button.addEventListener('click', createRipple);
    });
}

// ============================================
// TYPING INDICATOR FOR BOT MESSAGES
// ============================================
function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.classList.add('message', 'bot-message', 'typing-indicator');
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = `
        <div class="message-icon">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content typing-dots">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

// Profile Menu Functions
function toggleProfileMenu() {
    const profileMenu = document.getElementById('profileMenu');
    if (profileMenu) {
        profileMenu.classList.toggle('active');
    }
}

function closeProfileMenu() {
    const profileMenu = document.getElementById('profileMenu');
    if (profileMenu) {
        profileMenu.classList.remove('active');
    }
}

// Theme Toggle Functions
function toggleTheme() {
    const body = document.body;
    const currentTheme = body.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Update icon and text
    updateThemeUI(newTheme);
}

function updateThemeUI(theme) {
    const themeIcons = document.querySelectorAll('.theme-icon');
    const themeTexts = document.querySelectorAll('.theme-text');
    
    themeIcons.forEach(icon => {
        if (theme === 'light') {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        }
    });
    
    themeTexts.forEach(text => {
        text.textContent = theme === 'light' ? 'Light Theme' : 'Dark Theme';
    });
}

function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.body.setAttribute('data-theme', savedTheme);
    updateThemeUI(savedTheme);
}

// Close menu when clicking outside
document.addEventListener('click', function(event) {
    const profileDropdown = document.querySelector('.profile-dropdown');
    const profileMenu = document.getElementById('profileMenu');
    
    if (profileDropdown && profileMenu && !profileDropdown.contains(event.target)) {
        profileMenu.classList.remove('active');
    }
});

// Authentication Functions
async function handleLogout() {
    if (!confirm('Are you sure you want to logout?')) {
        return;
    }
    
    try {
        const response = await fetch('/api/auth/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            window.location.href = '/login';
        } else {
            alert('Logout failed. Please try again.');
        }
    } catch (error) {
        console.error('Logout error:', error);
        alert('An error occurred during logout.');
    }
}

// Welcome Popup Functions
function showWelcomePopup() {
    const welcomePopup = document.getElementById('welcomePopup');
    if (welcomePopup) {
        // Check if user has already seen the popup this session
        const hasSeenPopup = sessionStorage.getItem('hasSeenWelcomePopup');
        if (!hasSeenPopup) {
            welcomePopup.classList.remove('hidden');
        }
    }
}

function closeWelcomePopup() {
    const welcomePopup = document.getElementById('welcomePopup');
    if (welcomePopup) {
        welcomePopup.classList.add('hidden');
        // Mark as seen for this session
        sessionStorage.setItem('hasSeenWelcomePopup', 'true');
    }
}

function continueAsGuest() {
    closeWelcomePopup();
    // Optional: Show a brief notification
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        const guestNotification = document.createElement('div');
        guestNotification.className = 'message bot-message';
        guestNotification.innerHTML = `
            <i class="fas fa-robot message-icon"></i>
            <div class="message-content">
                <p>Welcome, Guest! 👋</p>
                <p>You're using Learnova in guest mode. All features are available, but your progress won't be saved.</p>
                <p>Click <strong>Sign Up</strong> anytime to save your progress!</p>
            </div>
        `;
        chatMessages.appendChild(guestNotification);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

// DOM Elements
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const chatMessages = document.getElementById('chatMessages');
const uploadBtn = document.getElementById('uploadBtn');
const fileInput = document.getElementById('fileInput');
const fileAttachment = document.getElementById('fileAttachment');
const fileName = document.getElementById('fileName');
const removeFileBtn = document.getElementById('removeFile');
const timerDisplay = document.getElementById('timerDisplay');
const startTimerBtn = document.getElementById('startTimer');
const pauseTimerBtn = document.getElementById('pauseTimer');
const resetTimerBtn = document.getElementById('resetTimer');
const presetBtns = document.querySelectorAll('.preset-btn');
const loadingSpinner = document.getElementById('loadingSpinner');
const quizModal = document.getElementById('quizModal');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeTheme(); // Load saved theme
    initializeRippleEffects(); // Add ripple effects to buttons
    setupEventListeners();
    updateTimerDisplay();
    
    // Show welcome popup for guests
    setTimeout(showWelcomePopup, 500); // Small delay for better UX
    
    // Add entrance animations to feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach((card, index) => {
        card.style.animation = `slideUp 0.6s ease ${index * 0.1}s backwards`;
    });
});

// Event Listeners
function setupEventListeners() {
    // Chat
    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    // File Upload
    uploadBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);
    removeFileBtn.addEventListener('click', removeFile);

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
    if (!message && !uploadedFile) return;

    // Add user message
    if (message) {
        addMessage(message, 'user');
    }
    if (uploadedFile) {
        addMessage(`📎 Attached: ${uploadedFile.name}`, 'user');
    }
    chatInput.value = '';

    // Show typing indicator
    showTypingIndicator();

    try {
        const formData = new FormData();
        formData.append('message', message);
        if (uploadedFile) {
            formData.append('file', uploadedFile);
        }

        const response = await fetch('/api/chat', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        hideTypingIndicator();

        if (data.success) {
            addMessage(data.response, 'bot');
            // Clear uploaded file after sending
            if (uploadedFile) {
                removeFile();
            }
        } else {
            addMessage('Sorry, I encountered an error. Please try again!', 'bot');
        }
    } catch (error) {
        hideTypingIndicator();
        console.error('Chat error:', error);
        addMessage('Connection error. Please check your connection and try again.', 'bot');
    }
}

// File Upload Functions
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    // Check file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
        alert('File size must be less than 10MB');
        return;
    }

    uploadedFile = file;
    fileName.textContent = file.name;
    fileAttachment.classList.add('active');
}

function removeFile() {
    uploadedFile = null;
    fileInput.value = '';
    fileName.textContent = 'No file selected';
    fileAttachment.classList.remove('active');
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

