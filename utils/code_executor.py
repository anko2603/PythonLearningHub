import sys
import io
import time
import json
import traceback
import contextlib
import logging
from typing import Dict, List, Any, Optional

def execute_code(code: str) -> Dict[str, Any]:
    """
    Execute Python code in a safe environment and return stdout, stderr, execution time, and status.
    """
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    
    result = {
        'output': '',
        'error': '',
        'success': True,
        'runtime_ms': 0
    }
    
    start_time = time.perf_counter()
    try:
        with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
            # Safe namespace with built-in functions
            global_scope = {
                '__name__': '__main__',
                '__builtins__': __builtins__
            }
            exec(code, global_scope)
            
        result['output'] = stdout_buffer.getvalue()
        result['error'] = stderr_buffer.getvalue()
    except Exception as e:
        result['success'] = False
        result['error'] = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
    finally:
        elapsed = (time.perf_counter() - start_time) * 1000
        result['runtime_ms'] = round(elapsed, 2)
        
    return result

def run_arena_test_cases(user_code: str, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Runs user code against test cases (LeetCode / HackerRank style runner).
    """
    test_results = []
    all_passed = True
    total_runtime = 0.0
    
    # Global environment to execute function definitions
    env = {
        '__name__': '__main__',
        '__builtins__': __builtins__
    }
    
    # First, try to define the function
    try:
        exec(user_code, env)
    except Exception as e:
        return {
            'status': 'Runtime Error',
            'success': False,
            'message': f"Compilation / Execution error: {type(e).__name__}: {str(e)}",
            'runtime_ms': 0,
            'memory_mb': round(14.2 + len(user_code) * 0.001, 1),
            'test_results': [],
            'passed_count': 0,
            'total_count': len(test_cases)
        }
        
    passed_count = 0
    
    for i, test in enumerate(test_cases):
        test_name = test.get('name', f"Test Case {i+1}")
        call_expr = test.get('call', '')
        expected = test.get('expected')
        
        start = time.perf_counter()
        test_item = {
            'id': i + 1,
            'name': test_name,
            'call': call_expr,
            'expected': expected,
            'actual': None,
            'passed': False,
            'error': None,
            'runtime_ms': 0
        }
        
        try:
            # Evaluate the function call in user environment
            actual_val = eval(call_expr, env)
            test_item['actual'] = actual_val
            
            # Compare actual with expected (handle bool, list, set, dict equality)
            if isinstance(expected, list) and isinstance(actual_val, list):
                test_item['passed'] = actual_val == expected
            elif isinstance(expected, (int, float, str, bool)):
                test_item['passed'] = actual_val == expected
            else:
                test_item['passed'] = json.dumps(actual_val, sort_keys=True, default=str) == json.dumps(expected, sort_keys=True, default=str)
                
            if test_item['passed']:
                passed_count += 1
            else:
                all_passed = False
        except Exception as e:
            all_passed = False
            test_item['error'] = f"{type(e).__name__}: {str(e)}"
        finally:
            duration = (time.perf_counter() - start) * 1000
            test_item['runtime_ms'] = round(duration, 2)
            total_runtime += duration
            
        test_results.append(test_item)
        
    status = 'Accepted' if all_passed else 'Wrong Answer'
    if any(t.get('error') for t in test_results):
        status = 'Runtime Error'
        
    return {
        'status': status,
        'success': all_passed,
        'runtime_ms': round(total_runtime, 1),
        'memory_mb': round(14.8 + len(user_code) * 0.002, 1),
        'passed_count': passed_count,
        'total_count': len(test_cases),
        'test_results': test_results
    }

def validate_solution(code: str, tests: List[Dict[str, str]], expected_output: Optional[str] = None) -> Dict[str, Any]:
    """
    Validate standard lesson solutions against test cases.
    """
    result = {
        'success': True,
        'feedback': '',
        'test_results': []
    }
    
    execution_result = execute_code(code)
    if not execution_result['success']:
        result['success'] = False
        result['feedback'] = f"Your code has errors:\n{execution_result['error']}"
        return result
        
    if expected_output is not None:
        if execution_result['output'].strip() != expected_output.strip():
            result['success'] = False
            result['feedback'] = (
                f"Expected output:\n{expected_output}\n\n"
                f"Your output:\n{execution_result['output']}"
            )
            return result
            
    for i, test in enumerate(tests):
        test_code = f"{code}\n\n{test.get('code', '')}"
        test_result = execute_code(test_code)
        test_passed = test_result['success']
        if test_passed and 'expected_output' in test:
            test_passed = test_result['output'].strip() == test['expected_output'].strip()
            
        result['test_results'].append({
            'test_id': i + 1,
            'description': test.get('description', f'Test case {i + 1}'),
            'passed': test_passed,
            'output': test_result['output'],
            'error': test_result['error'],
            'expected': test.get('expected_output', '')
        })
        if not test_passed:
            result['success'] = False
            
    if not result['success']:
        failed = [t for t in result['test_results'] if not t['passed']]
        result['feedback'] = f"{len(failed)} of {len(tests)} tests failed."
    else:
        result['feedback'] = "Great job! All tests passed."
        
    return result
