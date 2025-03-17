document.addEventListener('DOMContentLoaded', function() {
  // Initialize tooltips and popovers
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
  
  const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
  popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });
  
  // Handle quiz functionality
  document.querySelectorAll('.quiz-option').forEach(option => {
    option.addEventListener('click', function() {
      const quizContainer = this.closest('.quiz-container');
      const options = quizContainer.querySelectorAll('.quiz-option');
      const feedback = quizContainer.querySelector('.quiz-feedback');
      const isCorrect = this.dataset.correct === 'true';
      
      // Reset all options
      options.forEach(opt => {
        opt.classList.remove('correct', 'incorrect');
        opt.classList.add('disabled');
      });
      
      // Mark the selected option
      if (isCorrect) {
        this.classList.add('correct');
        feedback.innerHTML = '<div class="alert alert-success mt-3">Correct answer!</div>';
      } else {
        this.classList.add('incorrect');
        
        // Show the correct answer
        options.forEach(opt => {
          if (opt.dataset.correct === 'true') {
            opt.classList.add('correct');
          }
        });
        
        feedback.innerHTML = '<div class="alert alert-danger mt-3">Incorrect. See the correct answer highlighted.</div>';
      }
      
      feedback.style.display = 'block';
    });
  });
  
  // Handle code examples (syntax highlighting for static code)
  document.querySelectorAll('pre code').forEach((block) => {
    hljs.highlightElement(block);
  });
  
  // Initialize tab navigation if present
  const tabTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tab"]'));
  tabTriggerList.map(function (tabTriggerEl) {
    return new bootstrap.Tab(tabTriggerEl);
  });
});

// Function to initialize Python editor
function initializeEditor(editorId, outputId, runButtonId) {
  return new PythonEditor(editorId, outputId, runButtonId);
}

// Function to initialize problem solution checker
function initializeProblemChecker(editorId, outputId, checkButtonId, tests, expectedOutput) {
  const editor = new PythonEditor(editorId, outputId, null);
  const checkButton = document.getElementById(checkButtonId);
  
  if (checkButton) {
    checkButton.addEventListener('click', () => {
      editor.validateSolution(tests, expectedOutput);
    });
  }
  
  return editor;
}
