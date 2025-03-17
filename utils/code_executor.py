import sys
import io
import traceback
import contextlib
import logging
from typing import Dict, List, Any, Optional

def execute_code(code: str) -> Dict[str, Any]:
    """
    Execute Python code in a safe environment and return stdout, stderr, and any error messages.
    
    Args:
        code: The Python code to execute
        
    Returns:
        Dictionary with output, error, and success status
    """
    # Capture stdout and stderr
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    
    result = {
        'output': '',
        'error': '',
        'success': True
    }
    
    try:
        # Use contextlib to redirect stdout and stderr
        with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
            # Execute the code
            exec(code, {})
            
        result['output'] = stdout_buffer.getvalue()
        result['error'] = stderr_buffer.getvalue()
    
    except Exception as e:
        result['success'] = False
        result['error'] = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
    
    return result

def validate_solution(code: str, tests: List[Dict[str, str]], expected_output: Optional[str] = None) -> Dict[str, Any]:
    """
    Validate a user's solution against test cases and expected output.
    
    Args:
        code: The user's Python code
        tests: List of test cases, each with input and expected output
        expected_output: Optional expected output for the code
        
    Returns:
        Dictionary with validation results and feedback
    """
    result = {
        'success': True,
        'feedback': '',
        'test_results': []
    }
    
    # First, check if the code runs without errors
    execution_result = execute_code(code)
    
    if not execution_result['success']:
        result['success'] = False
        result['feedback'] = f"Your code has errors:\n{execution_result['error']}"
        return result
    
    # If expected output is provided, check if it matches
    if expected_output is not None:
        if execution_result['output'].strip() != expected_output.strip():
            result['success'] = False
            result['feedback'] = (
                f"Expected output:\n{expected_output}\n\n"
                f"Your output:\n{execution_result['output']}"
            )
            return result
    
    # Run each test case
    for i, test in enumerate(tests):
        test_code = f"{code}\n\n{test['code']}"
        test_result = execute_code(test_code)
        
        test_passed = test_result['success']
        if test_passed and 'expected_output' in test:
            test_passed = test_result['output'].strip() == test['expected_output'].strip()
        
        test_outcome = {
            'test_id': i + 1,
            'description': test.get('description', f'Test case {i + 1}'),
            'passed': test_passed,
            'output': test_result['output'],
            'error': test_result['error'],
            'expected': test.get('expected_output', '')
        }
        
        result['test_results'].append(test_outcome)
        
        if not test_passed:
            result['success'] = False
    
    # Generate feedback based on test results
    if not result['success']:
        failed_tests = [t for t in result['test_results'] if not t['passed']]
        result['feedback'] = f"{len(failed_tests)} of {len(tests)} tests failed. Check the test results for details."
    else:
        result['feedback'] = "Great job! All tests passed."
    
    return result
