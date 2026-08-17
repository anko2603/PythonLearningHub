// LeetCode / HackerRank Problem Arena Workspace Engine
document.addEventListener('DOMContentLoaded', () => {
  const editorTextarea = document.getElementById('arena-code-editor');
  if (!editorTextarea) return;

  const problemId = document.getElementById('arena-problem-id')?.value;
  const runBtn = document.getElementById('btn-run-code');
  const submitBtn = document.getElementById('btn-submit-code');
  const resetBtn = document.getElementById('btn-reset-code');
  const outputContainer = document.getElementById('arena-console-output');
  const starterCode = editorTextarea.value;

  // Initialize CodeMirror with Dracula/OLED theme
  const editor = CodeMirror.fromTextArea(editorTextarea, {
    mode: 'python',
    theme: 'dracula',
    lineNumbers: true,
    indentUnit: 4,
    tabSize: 4,
    indentWithTabs: false,
    autoCloseBrackets: true,
    matchBrackets: true,
    lineWrapping: true,
    extraKeys: {
      "Tab": function(cm) {
        cm.replaceSelection("    ", "end");
      }
    }
  });

  // Local storage cache for user's work
  const storageKey = `arena_code_${problemId}`;
  const savedCode = localStorage.getItem(storageKey);
  if (savedCode) {
    editor.setValue(savedCode);
  }

  editor.on('change', () => {
    localStorage.setItem(storageKey, editor.getValue());
  });

  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      if (confirm('Reset code back to starting template?')) {
        editor.setValue(starterCode);
        localStorage.removeItem(storageKey);
      }
    });
  }

  // Tab switching logic for Left Panel (Description, Hints, Solutions)
  const leftTabs = document.querySelectorAll('.left-panel-tab');
  leftTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      leftTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const targetId = tab.getAttribute('data-target');
      document.querySelectorAll('.left-tab-pane').forEach(pane => pane.classList.add('d-none'));
      document.getElementById(targetId)?.classList.remove('d-none');
    });
  });

  // Tab switching for Right Panel (Code, Console Output)
  const rightTabs = document.querySelectorAll('.right-panel-tab');
  rightTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      rightTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const targetId = tab.getAttribute('data-target');
      document.querySelectorAll('.right-tab-pane').forEach(pane => pane.classList.add('d-none'));
      document.getElementById(targetId)?.classList.remove('d-none');
    });
  });

  function showConsoleTab() {
    const consoleTabBtn = document.querySelector('[data-target="pane-console"]');
    if (consoleTabBtn) consoleTabBtn.click();
  }

  function setLoading(btn, isLoading, text) {
    if (isLoading) {
      btn.disabled = true;
      btn.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status"></span>${text}`;
    } else {
      btn.disabled = false;
      btn.innerHTML = text;
    }
  }

  // Trigger celebration confetti
  function triggerCelebration() {
    if (typeof confetti === 'function') {
      confetti({
        particleCount: 80,
        spread: 70,
        origin: { y: 0.6 }
      });
    }
  }

  // Run visible Sample Test Cases
  if (runBtn) {
    runBtn.addEventListener('click', async () => {
      showConsoleTab();
      setLoading(runBtn, true, 'Running...');
      outputContainer.innerHTML = '<div class="text-muted p-2"><i class="bi bi-hourglass-split me-2"></i>Evaluating sample test cases...</div>';

      try {
        const response = await fetch('/api/arena/run', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            problem_id: problemId,
            code: editor.getValue()
          })
        });
        const data = await response.json();
        renderResults(data, false);
      } catch (err) {
        outputContainer.innerHTML = `<div class="text-danger p-2">Network Error: ${err.message}</div>`;
      } finally {
        setLoading(runBtn, false, '<i class="bi bi-play-fill me-1"></i>Run Code');
      }
    });
  }

  // Submit against complete Test Suite (hidden + sample)
  if (submitBtn) {
    submitBtn.addEventListener('click', async () => {
      showConsoleTab();
      setLoading(submitBtn, true, 'Submitting...');
      outputContainer.innerHTML = '<div class="text-muted p-2"><i class="bi bi-cpu me-2"></i>Running full automated test suite...</div>';

      try {
        const response = await fetch('/api/arena/submit', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            problem_id: problemId,
            code: editor.getValue()
          })
        });
        const data = await response.json();
        renderResults(data, true);
        if (data.status === 'Accepted') {
          triggerCelebration();
        }
      } catch (err) {
        outputContainer.innerHTML = `<div class="text-danger p-2">Network Error: ${err.message}</div>`;
      } finally {
        setLoading(submitBtn, false, '<i class="bi bi-cloud-arrow-up-fill me-1"></i>Submit');
      }
    });
  }

  function renderResults(data, isSubmission) {
    if (!data.test_results || data.test_results.length === 0) {
      outputContainer.innerHTML = `
        <div class="p-3 bg-danger bg-opacity-10 border border-danger rounded">
          <div class="fw-bold text-danger mb-2"><i class="bi bi-exclamation-triangle-fill me-2"></i>${data.status || 'Error'}</div>
          <pre class="text-danger mb-0">${data.message || 'Execution failed'}</pre>
        </div>
      `;
      return;
    }

    const isAccepted = data.status === 'Accepted';
    const statusColor = isAccepted ? 'text-success' : 'text-danger';
    const statusBg = isAccepted ? 'bg-success' : 'bg-danger';

    let html = `
      <div class="mb-3 p-3 rounded bg-elevated border border-color">
        <div class="d-flex align-items-center justify-content-between mb-2">
          <div class="fs-5 fw-bold ${statusColor}">
            <i class="bi bi-${isAccepted ? 'check-circle-fill' : 'x-circle-fill'} me-2"></i>${data.status}
          </div>
          <div class="d-flex gap-2">
            <span class="badge bg-dark border border-secondary text-muted">
              <i class="bi bi-clock me-1"></i>${data.runtime_ms} ms
            </span>
            <span class="badge bg-dark border border-secondary text-muted">
              <i class="bi bi-memory me-1"></i>${data.memory_mb} MB
            </span>
            <span class="badge ${statusBg} bg-opacity-25 text-white border">
              ${data.passed_count}/${data.total_count} Passed
            </span>
          </div>
        </div>
        ${isAccepted && isSubmission ? '<div class="text-success small fw-medium">🎉 Congratulations! You have solved this problem efficiently.</div>' : ''}
      </div>
    `;

    html += '<div class="d-flex flex-column gap-2">';
    data.test_results.forEach(test => {
      const pass = test.passed;
      html += `
        <div class="p-3 rounded border ${pass ? 'border-success bg-success bg-opacity-10' : 'border-danger bg-danger bg-opacity-10'}">
          <div class="d-flex justify-content-between align-items-center mb-1">
            <span class="fw-semibold ${pass ? 'text-success' : 'text-danger'}">
              <i class="bi bi-${pass ? 'check' : 'x'}-lg me-1"></i>${test.name}
            </span>
            <small class="text-muted">${test.runtime_ms}ms</small>
          </div>
          <div class="small font-monospace mb-1 text-muted">Input Call: <code>${test.call}</code></div>
          ${!pass ? `
            <div class="small font-monospace mt-2">
              <div class="text-secondary">Expected: <span class="text-light">${JSON.stringify(test.expected)}</span></div>
              <div class="text-secondary">Actual: <span class="text-danger">${JSON.stringify(test.actual)}</span></div>
              ${test.error ? `<div class="text-danger mt-1">Error: ${test.error}</div>` : ''}
            </div>
          ` : ''}
        </div>
      `;
    });
    html += '</div>';

    outputContainer.innerHTML = html;
  }
});
