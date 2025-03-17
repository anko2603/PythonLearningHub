class PythonEditor {
  constructor(editorId, outputId, runButtonId) {
    this.editorId = editorId;
    this.outputId = outputId;
    this.runButtonId = runButtonId;
    this.editor = null;
    this.output = document.getElementById(outputId);
    this.runButton = document.getElementById(runButtonId);
    
    this.initialize();
  }
  
  initialize() {
    // Initialize CodeMirror editor
    this.editor = CodeMirror.fromTextArea(document.getElementById(this.editorId), {
      mode: 'python',
      theme: 'dracula',
      lineNumbers: true,
      indentUnit: 4,
      tabSize: 4,
      indentWithTabs: false,
      autoCloseBrackets: true,
      matchBrackets: true,
      extraKeys: {
        "Tab": function(cm) {
          cm.replaceSelection("    ", "end");
        }
      }
    });
    
    // Set up event listeners
    if (this.runButton) {
      this.runButton.addEventListener('click', () => this.runCode());
    }
  }
  
  getCode() {
    return this.editor.getValue();
  }
  
  setCode(code) {
    this.editor.setValue(code);
  }
  
  showLoading() {
    if (this.output) {
      this.output.innerHTML = '<div class="d-flex justify-content-center"><div class="spinner-border text-light" role="status"><span class="visually-hidden">Loading...</span></div></div>';
    }
  }
  
  displayOutput(result) {
    if (!this.output) return;
    
    let outputHtml = '';
    
    if (result.success) {
      if (result.output) {
        outputHtml += `<pre class="output-area p-3 rounded bg-dark text-light">${this._escapeHtml(result.output)}</pre>`;
      } else {
        outputHtml += '<div class="alert alert-info">Code executed successfully with no output.</div>';
      }
    } else {
      outputHtml += `<div class="alert alert-danger"><strong>Error:</strong><pre class="mb-0 text-danger">${this._escapeHtml(result.error)}</pre></div>`;
    }
    
    this.output.innerHTML = outputHtml;
  }
  
  displayTestResults(result) {
    if (!this.output) return;
    
    let outputHtml = `<div class="alert alert-${result.success ? 'success' : 'danger'}">${result.feedback}</div>`;
    
    if (result.test_results && result.test_results.length > 0) {
      outputHtml += '<div class="list-group mb-3">';
      
      for (const test of result.test_results) {
        const statusClass = test.passed ? 'success' : 'danger';
        const statusIcon = test.passed ? 'check-circle-fill' : 'x-circle-fill';
        
        outputHtml += `
          <div class="list-group-item list-group-item-${statusClass}">
            <div class="d-flex w-100 justify-content-between">
              <h5 class="mb-1">
                <i class="bi bi-${statusIcon} me-2"></i>
                ${this._escapeHtml(test.description)}
              </h5>
              <small>${test.passed ? 'Passed' : 'Failed'}</small>
            </div>
            ${!test.passed ? `
              <div class="mt-2">
                <div class="mb-1"><strong>Expected:</strong></div>
                <pre class="p-2 bg-dark text-light rounded">${this._escapeHtml(test.expected)}</pre>
                <div class="mb-1 mt-2"><strong>Actual:</strong></div>
                <pre class="p-2 bg-dark text-light rounded">${this._escapeHtml(test.output)}</pre>
                ${test.error ? `
                  <div class="mb-1 mt-2"><strong>Error:</strong></div>
                  <pre class="p-2 bg-danger text-light rounded">${this._escapeHtml(test.error)}</pre>
                ` : ''}
              </div>
            ` : ''}
          </div>
        `;
      }
      
      outputHtml += '</div>';
    }
    
    this.output.innerHTML = outputHtml;
  }
  
  runCode() {
    const code = this.getCode();
    if (!code.trim()) {
      this.output.innerHTML = '<div class="alert alert-warning">Please enter some code to run.</div>';
      return;
    }
    
    this.showLoading();
    
    // Send the code to the server for execution
    fetch('/execute', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ code })
    })
    .then(response => response.json())
    .then(result => {
      this.displayOutput(result);
    })
    .catch(error => {
      this.output.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
    });
  }
  
  validateSolution(tests, expectedOutput) {
    const code = this.getCode();
    if (!code.trim()) {
      this.output.innerHTML = '<div class="alert alert-warning">Please enter some code to run.</div>';
      return;
    }
    
    this.showLoading();
    
    // Send the code to the server for validation
    fetch('/validate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 
        code,
        tests,
        expected_output: expectedOutput
      })
    })
    .then(response => response.json())
    .then(result => {
      this.displayTestResults(result);
    })
    .catch(error => {
      this.output.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
    });
  }
  
  // Helper methods
  _escapeHtml(text) {
    if (!text) return '';
    
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}
