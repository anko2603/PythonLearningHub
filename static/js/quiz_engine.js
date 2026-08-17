// Gamified Interactive Quiz Engine
document.addEventListener('DOMContentLoaded', () => {
  const quizContainer = document.getElementById('quiz-app-container');
  if (!quizContainer) return;

  const quizData = JSON.parse(document.getElementById('quiz-data-json').textContent);
  let currentQuestionIndex = 0;
  let userAnswers = {};
  let streakCount = 0;
  let maxStreak = 0;
  let earnedXp = 0;
  let timerSeconds = 0;
  let timerInterval = null;

  // DOM Elements
  const progressText = document.getElementById('quiz-progress-text');
  const progressBar = document.getElementById('quiz-progress-bar');
  const streakBadge = document.getElementById('quiz-streak-badge');
  const streakCountEl = document.getElementById('quiz-streak-count');
  const timerEl = document.getElementById('quiz-timer-text');
  const questionTitle = document.getElementById('quiz-question-title');
  const questionCodeBlock = document.getElementById('quiz-code-block');
  const questionCode = document.getElementById('quiz-code-text');
  const optionsContainer = document.getElementById('quiz-options-container');
  const explanationBox = document.getElementById('quiz-explanation-box');
  const explanationText = document.getElementById('quiz-explanation-text');
  const nextBtn = document.getElementById('quiz-next-btn');

  // Results Screen Elements
  const playScreen = document.getElementById('quiz-play-screen');
  const resultScreen = document.getElementById('quiz-result-screen');
  const finalScoreEl = document.getElementById('quiz-final-score');
  const finalXpEl = document.getElementById('quiz-final-xp');
  const finalStreakEl = document.getElementById('quiz-final-streak');
  const restartBtn = document.getElementById('quiz-restart-btn');

  // Start Timer
  function startTimer() {
    timerSeconds = 0;
    timerInterval = setInterval(() => {
      timerSeconds++;
      const mins = String(Math.floor(timerSeconds / 60)).padStart(2, '0');
      const secs = String(timerSeconds % 60).padStart(2, '0');
      if (timerEl) timerEl.textContent = `${mins}:${secs}`;
    }, 1000);
  }

  function triggerConfetti() {
    if (typeof confetti === 'function') {
      confetti({
        particleCount: 100,
        spread: 80,
        origin: { y: 0.6 }
      });
    }
  }

  function loadQuestion(index) {
    const q = quizData.questions[index];
    const total = quizData.questions.length;

    progressText.textContent = `Question ${index + 1} of ${total}`;
    progressBar.style.width = `${((index + 1) / total) * 100}%`;

    questionTitle.textContent = q.question;

    if (q.code) {
      questionCodeBlock.classList.remove('d-none');
      questionCode.textContent = q.code;
    } else {
      questionCodeBlock.classList.add('d-none');
    }

    explanationBox.classList.add('d-none');
    nextBtn.classList.add('d-none');

    // Render Options
    optionsContainer.innerHTML = '';
    const letters = ['A', 'B', 'C', 'D', 'E'];
    q.options.forEach((opt, idx) => {
      const card = document.createElement('div');
      card.className = 'quiz-option-card';
      card.innerHTML = `
        <div class="option-marker">${letters[idx]}</div>
        <div class="flex-grow-1 font-monospace">${opt}</div>
      `;
      card.addEventListener('click', () => handleOptionSelect(idx, card));
      optionsContainer.appendChild(card);
    });
  }

  function handleOptionSelect(selectedIndex, selectedCard) {
    const q = quizData.questions[currentQuestionIndex];
    if (userAnswers[q.id] !== undefined) return; // already answered

    userAnswers[q.id] = selectedIndex;
    const isCorrect = selectedIndex === q.correct_answer;

    const cards = optionsContainer.querySelectorAll('.quiz-option-card');
    cards.forEach((card, idx) => {
      card.style.pointerEvents = 'none';
      if (idx === q.correct_answer) {
        card.classList.add('correct');
      } else if (idx === selectedIndex && !isCorrect) {
        card.classList.add('incorrect');
      }
    });

    if (isCorrect) {
      streakCount++;
      if (streakCount > maxStreak) maxStreak = streakCount;
      streakBadge.classList.remove('d-none');
      streakCountEl.textContent = `${streakCount}x Streak!`;
      if (streakCount >= 3) triggerConfetti();
    } else {
      streakCount = 0;
      streakBadge.classList.add('d-none');
    }

    // Show Explanation
    explanationText.textContent = q.explanation || (isCorrect ? 'Correct answer!' : 'Incorrect.');
    explanationBox.classList.remove('d-none');

    // Show Next Button
    nextBtn.classList.remove('d-none');
    if (currentQuestionIndex === quizData.questions.length - 1) {
      nextBtn.innerHTML = 'Finish Quiz & View Results <i class="bi bi-arrow-right ms-2"></i>';
    } else {
      nextBtn.innerHTML = 'Next Question <i class="bi bi-arrow-right ms-2"></i>';
    }
  }

  nextBtn.addEventListener('click', () => {
    if (currentQuestionIndex < quizData.questions.length - 1) {
      currentQuestionIndex++;
      loadQuestion(currentQuestionIndex);
    } else {
      finishQuiz();
    }
  });

  async function finishQuiz() {
    clearInterval(timerInterval);

    try {
      const res = await fetch('/api/quiz/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          quiz_id: quizData.id,
          answers: userAnswers
        })
      });
      const data = await res.json();

      playScreen.classList.add('d-none');
      resultScreen.classList.remove('d-none');

      finalScoreEl.textContent = `${data.score_percentage}%`;
      finalXpEl.textContent = `+${data.earned_xp} XP`;
      finalStreakEl.textContent = `${maxStreak}x`;

      if (data.score_percentage >= 70) {
        triggerConfetti();
      }
    } catch (e) {
      console.error('Error submitting quiz', e);
    }
  }

  if (restartBtn) {
    restartBtn.addEventListener('click', () => {
      userAnswers = {};
      currentQuestionIndex = 0;
      streakCount = 0;
      resultScreen.classList.add('d-none');
      playScreen.classList.remove('d-none');
      startTimer();
      loadQuestion(0);
    });
  }

  // Initialize
  startTimer();
  loadQuestion(0);
});
