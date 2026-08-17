// Global Command Palette (Ctrl+K / Cmd+K)
document.addEventListener('DOMContentLoaded', () => {
  const cmdModal = document.getElementById('commandPaletteModal');
  const cmdInput = document.getElementById('cmd-search-input');
  const cmdResults = document.getElementById('cmd-results-container');
  const searchTriggers = document.querySelectorAll('.cmd-palette-trigger');

  if (!cmdModal || !cmdInput) return;

  const bsModal = new bootstrap.Modal(cmdModal);

  const searchItems = [
    { title: 'LeetCode Arena - All Problems', url: '/arena', type: 'Arena', icon: 'code-slash' },
    { title: 'Two Sum Problem (Easy)', url: '/arena/two-sum', type: 'Problem', icon: 'lightning-charge' },
    { title: 'Valid Palindrome (Easy)', url: '/arena/valid-palindrome', type: 'Problem', icon: 'lightning-charge' },
    { title: 'Fizz Buzz Challenge (Easy)', url: '/arena/fizz-buzz', type: 'Problem', icon: 'lightning-charge' },
    { title: 'Valid Parentheses (Easy)', url: '/arena/valid-parentheses', type: 'Problem', icon: 'lightning-charge' },
    { title: 'Container With Most Water (Medium)', url: '/arena/container-with-most-water', type: 'Problem', icon: 'water' },
    { title: 'Longest Substring Without Repeating (Medium)', url: '/arena/longest-substring-without-repeating', type: 'Problem', icon: 'aspect-ratio' },
    { title: 'Trapping Rain Water (Hard)', url: '/arena/trapping-rain-water', type: 'Problem', icon: 'fire' },
    { title: 'Interactive Quiz Arena', url: '/quizzes', type: 'Quiz', icon: 'award' },
    { title: 'Python Core & Syntax Mastery Quiz', url: '/quiz/python-fundamentals', type: 'Quiz', icon: 'check-circle' },
    { title: 'Data Structures & Big-O Quiz', url: '/quiz/ds-algorithms-quiz', type: 'Quiz', icon: 'cpu' },
    { title: 'Tricky Python Quirks & Gotchas Quiz', url: '/quiz/tricky-python-gotchas', type: 'Quiz', icon: 'patch-question' },
    { title: 'Python Basics Track', url: '/track/beginner', type: 'Track', icon: 'book' },
    { title: 'Intermediate Python Track', url: '/track/intermediate', type: 'Track', icon: 'layers' },
    { title: 'Advanced Python Track', url: '/track/advanced', type: 'Track', icon: 'braces' },
    { title: 'Interactive Playground & Sandbox', url: '/playground', type: 'Tool', icon: 'terminal' }
  ];

  // Open on shortcut Ctrl+K or Cmd+K
  window.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      bsModal.show();
      setTimeout(() => cmdInput.focus(), 200);
    }
  });

  searchTriggers.forEach(btn => {
    btn.addEventListener('click', () => {
      bsModal.show();
      setTimeout(() => cmdInput.focus(), 200);
    });
  });

  cmdInput.addEventListener('input', () => {
    const q = cmdInput.value.toLowerCase().trim();
    const filtered = searchItems.filter(item => 
      item.title.toLowerCase().includes(q) || 
      item.type.toLowerCase().includes(q)
    );

    if (filtered.length === 0) {
      cmdResults.innerHTML = '<div class="p-4 text-center text-muted">No results found for "' + cmdInput.value + '"</div>';
      return;
    }

    let html = '';
    filtered.forEach(item => {
      html += `
        <a href="${item.url}" class="cmd-item">
          <div class="d-flex align-items-center gap-3">
            <div class="p-2 rounded bg-dark border border-secondary text-info">
              <i class="bi bi-${item.icon}"></i>
            </div>
            <div>
              <div class="fw-semibold text-light">${item.title}</div>
              <small class="text-muted">${item.type}</small>
            </div>
          </div>
          <i class="bi bi-arrow-right text-muted"></i>
        </a>
      `;
    });
    cmdResults.innerHTML = html;
  });
});
