import json
import logging
import subprocess
import tempfile
import os
import traceback
from flask import Markup

def load_content(file_path):
    """Load content from JSON file"""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error loading content from {file_path}: {str(e)}")
        return []

def get_tutorials(level=None):
    """Get tutorials, optionally filtered by level"""
    tutorials = load_content('content/tutorials.json')
    if level:
        return [t for t in tutorials if t.get('level') == level]
    return tutorials

def get_problems(level=None):
    """Get problems, optionally filtered by level"""
    problems = load_content('content/problems.json')
    if level:
        return [p for p in problems if p.get('level') == level]
    return problems

def get_quizzes(level=None):
    """Get quizzes, optionally filtered by level"""
    quizzes = load_content('content/quizzes.json')
    if level:
        return [q for q in quizzes if q.get('level') == level]
    return quizzes

def get_tutorial_by_id(tutorial_id):
    """Get a specific tutorial by ID"""
    tutorials = load_content('content/tutorials.json')
    for tutorial in tutorials:
        if tutorial.get('id') == tutorial_id:
            # Convert content to Markup to render HTML
            tutorial['content'] = Markup(tutorial['content'])
            return tutorial
    return None

def get_problem_by_id(problem_id):
    """Get a specific problem by ID"""
    problems = load_content('content/problems.json')
    for problem in problems:
        if problem.get('id') == problem_id:
            # Convert content to Markup to render HTML
            problem['content'] = Markup(problem['content'])
            return problem
    return None

def get_quiz_by_id(quiz_id):
    """Get a specific quiz by ID"""
    quizzes = load_content('content/quizzes.json')
    for quiz in quizzes:
        if quiz.get('id') == quiz_id:
            # Convert content to Markup to render HTML
            quiz['content'] = Markup(quiz['content'])
            return quiz
    return None

def execute_python_code(code):
    """Execute Python code and return the result"""
    result = {
        'output': '',
        'error': None,
        'success': False
    }
    
    # Create a temporary file to write the code
    with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp_file:
        temp_file_path = temp_file.name
        try:
            # Write the code to the temporary file
            temp_file.write(code.encode('utf-8'))
            temp_file.flush()
            
            # Execute the code with a timeout
            process = subprocess.Popen(
                ['python', temp_file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for the process to complete with a timeout
            stdout, stderr = process.communicate(timeout=5)
            
            if stderr:
                result['error'] = stderr
            else:
                result['output'] = stdout
                result['success'] = True
                
        except subprocess.TimeoutExpired:
            process.kill()
            result['error'] = "Execution timed out after 5 seconds"
        except Exception as e:
            result['error'] = str(e)
            logging.error(f"Error executing code: {traceback.format_exc()}")
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    return result

def check_solution(problem_id, user_code):
    """Check if the user's solution is correct for a given problem"""
    problem = get_problem_by_id(problem_id)
    if not problem:
        return {"success": False, "message": "Problem not found"}
    
    # Get the test cases from the problem
    test_cases = problem.get('test_cases', [])
    
    if not test_cases:
        # If no test cases, just execute the code
        result = execute_python_code(user_code)
        return result
    
    # Create a temporary file with the user's code and test cases
    full_code = user_code + "\n\n" + "\n".join(test_cases)
    result = execute_python_code(full_code)
    
    if result['success']:
        return {"success": True, "message": "All tests passed!", "output": result['output']}
    else:
        return {"success": False, "message": "Tests failed", "error": result['error']}
