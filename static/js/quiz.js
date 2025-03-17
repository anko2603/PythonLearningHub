document.addEventListener('DOMContentLoaded', function() {
    // Initialize quiz functionality
    initializeQuiz();
    
    function initializeQuiz() {
        const quizForm = document.getElementById('quiz-form');
        const quizSubmitBtn = document.getElementById('quiz-submit');
        
        if (!quizForm || !quizSubmitBtn) return;
        
        // Set up option selection
        const optionElements = document.querySelectorAll('.quiz-option');
        optionElements.forEach(option => {
            option.addEventListener('click', function() {
                const questionId = this.getAttribute('data-question-id');
                const optionValue = this.getAttribute('data-option-value');
                
                // Remove selected class from all options in the same question
                document.querySelectorAll(`.quiz-option[data-question-id="${questionId}"]`)
                    .forEach(el => el.classList.remove('selected'));
                
                // Add selected class to clicked option
                this.classList.add('selected');
                
                // Update hidden input with selected answer
                const hiddenInput = document.querySelector(`input[name="answer-${questionId}"]`);
                if (hiddenInput) {
                    hiddenInput.value = optionValue;
                }
            });
        });
        
        // Handle quiz submission
        quizSubmitBtn.addEventListener('click', function(e) {
            e.preventDefault();
            submitQuiz();
        });
    }
    
    function submitQuiz() {
        const quizId = document.getElementById('quiz-id')?.value;
        const resultDiv = document.getElementById('quiz-result');
        const loader = document.querySelector('.loader');
        
        if (!quizId) return;
        
        // Collect all answers
        const answers = {};
        const answerInputs = document.querySelectorAll('input[name^="answer-"]');
        answerInputs.forEach(input => {
            const questionId = input.getAttribute('name').replace('answer-', '');
            answers[questionId] = input.value;
        });
        
        // Check if all questions are answered
        const totalQuestions = document.querySelectorAll('.quiz-question').length;
        if (Object.keys(answers).length < totalQuestions) {
            showQuizMessage('Please answer all questions before submitting.', false);
            return;
        }
        
        // Show loading indicator
        if (loader) loader.style.display = 'block';
        if (resultDiv) resultDiv.innerHTML = '';
        
        // Send answers to backend for checking
        fetch('/check_quiz', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ quiz_id: quizId, answers: answers }),
        })
        .then(response => response.json())
        .then(data => {
            if (loader) loader.style.display = 'none';
            
            if (data.error) {
                showQuizMessage(data.error, false);
            } else {
                const scorePercentage = data.score.toFixed(0);
                let message = `You scored ${data.correct} out of ${data.total} (${scorePercentage}%)`;
                let success = data.score >= 70; // Success if 70% or higher
                
                showQuizMessage(message, success);
                
                if (resultDiv) {
                    let resultHtml = `<div class="mt-4 p-3 ${success ? 'bg-success' : 'bg-danger'} bg-opacity-25 rounded">`;
                    resultHtml += `<h4>Your Score: ${scorePercentage}%</h4>`;
                    resultHtml += `<p>You answered ${data.correct} out of ${data.total} questions correctly.</p>`;
                    
                    if (success) {
                        resultHtml += `<p>Great job! You've mastered this quiz.</p>`;
                    } else {
                        resultHtml += `<p>Keep practicing! Try reviewing the material and attempt the quiz again.</p>`;
                    }
                    
                    resultHtml += `</div>`;
                    resultDiv.innerHTML = resultHtml;
                }
                
                // Disable submit button after successful submission
                const submitBtn = document.getElementById('quiz-submit');
                if (submitBtn) {
                    submitBtn.disabled = true;
                }
            }
        })
        .catch(error => {
            if (loader) loader.style.display = 'none';
            showQuizMessage('Error: ' + error.message, false);
        });
    }
    
    function showQuizMessage(message, success) {
        const messageDiv = document.getElementById('quiz-message');
        if (messageDiv) {
            messageDiv.className = success ? 'result-success' : 'result-error';
            messageDiv.textContent = message;
            messageDiv.style.display = 'block';
            
            // Scroll to message
            messageDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }
});
