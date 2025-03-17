from flask import render_template, request, jsonify, redirect, url_for
from app import app
from utils import (
    get_tutorials, get_problems, get_quizzes,
    get_tutorial_by_id, get_problem_by_id, get_quiz_by_id,
    execute_python_code, check_solution
)

@app.route('/')
def index():
    """Homepage view with overview of topics and levels"""
    beginner_tutorials = get_tutorials(level='beginner')[:3]
    intermediate_tutorials = get_tutorials(level='intermediate')[:3]
    advanced_tutorials = get_tutorials(level='advanced')[:3]
    
    return render_template('index.html', 
                           beginner_tutorials=beginner_tutorials,
                           intermediate_tutorials=intermediate_tutorials,
                           advanced_tutorials=advanced_tutorials)

@app.route('/tutorials')
def tutorials():
    """All tutorials view"""
    level = request.args.get('level')
    tutorials_list = get_tutorials(level)
    return render_template('index.html', 
                           active_tab='tutorials',
                           tutorials=tutorials_list,
                           current_level=level)

@app.route('/tutorial/<tutorial_id>')
def tutorial(tutorial_id):
    """Individual tutorial view"""
    tutorial_content = get_tutorial_by_id(tutorial_id)
    if not tutorial_content:
        return redirect(url_for('index'))
    
    # Get next and previous tutorials for navigation
    all_tutorials = get_tutorials()
    tutorial_ids = [t.get('id') for t in all_tutorials]
    try:
        current_index = tutorial_ids.index(tutorial_id)
        prev_id = tutorial_ids[current_index - 1] if current_index > 0 else None
        next_id = tutorial_ids[current_index + 1] if current_index < len(tutorial_ids) - 1 else None
    except ValueError:
        prev_id, next_id = None, None
    
    return render_template('tutorial.html', 
                           tutorial=tutorial_content,
                           prev_id=prev_id,
                           next_id=next_id)

@app.route('/problems')
def problems():
    """All problems view"""
    level = request.args.get('level')
    problems_list = get_problems(level)
    return render_template('index.html', 
                           active_tab='problems',
                           problems=problems_list,
                           current_level=level)

@app.route('/problem/<problem_id>')
def problem(problem_id):
    """Individual problem view"""
    problem_content = get_problem_by_id(problem_id)
    if not problem_content:
        return redirect(url_for('index'))
    
    # Get next and previous problems for navigation
    all_problems = get_problems()
    problem_ids = [p.get('id') for p in all_problems]
    try:
        current_index = problem_ids.index(problem_id)
        prev_id = problem_ids[current_index - 1] if current_index > 0 else None
        next_id = problem_ids[current_index + 1] if current_index < len(problem_ids) - 1 else None
    except ValueError:
        prev_id, next_id = None, None
    
    return render_template('problem.html', 
                           problem=problem_content,
                           prev_id=prev_id,
                           next_id=next_id)

@app.route('/quizzes')
def quizzes():
    """All quizzes view"""
    level = request.args.get('level')
    quizzes_list = get_quizzes(level)
    return render_template('index.html', 
                           active_tab='quizzes',
                           quizzes=quizzes_list,
                           current_level=level)

@app.route('/quiz/<quiz_id>')
def quiz(quiz_id):
    """Individual quiz view"""
    quiz_content = get_quiz_by_id(quiz_id)
    if not quiz_content:
        return redirect(url_for('index'))
    
    return render_template('quiz.html', quiz=quiz_content)

@app.route('/about')
def about():
    """About page with information about the learning platform"""
    return render_template('about.html')

@app.route('/execute', methods=['POST'])
def execute():
    """API endpoint to execute Python code"""
    code = request.json.get('code', '')
    if not code:
        return jsonify({"error": "No code provided"}), 400
    
    result = execute_python_code(code)
    return jsonify(result)

@app.route('/check_solution', methods=['POST'])
def check_solution_route():
    """API endpoint to check a problem solution"""
    problem_id = request.json.get('problem_id')
    user_code = request.json.get('code', '')
    
    if not problem_id or not user_code:
        return jsonify({"error": "Problem ID and code are required"}), 400
    
    result = check_solution(problem_id, user_code)
    return jsonify(result)

@app.route('/check_quiz', methods=['POST'])
def check_quiz_route():
    """API endpoint to check quiz answers"""
    quiz_id = request.json.get('quiz_id')
    answers = request.json.get('answers', {})
    
    if not quiz_id or not answers:
        return jsonify({"error": "Quiz ID and answers are required"}), 400
    
    quiz = get_quiz_by_id(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404
    
    correct_answers = 0
    total_questions = len(quiz.get('questions', []))
    
    for q_id, user_answer in answers.items():
        for question in quiz.get('questions', []):
            if str(question.get('id')) == q_id and user_answer == question.get('correct_answer'):
                correct_answers += 1
                break
    
    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    
    return jsonify({
        "success": True,
        "score": score,
        "correct": correct_answers,
        "total": total_questions
    })

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('index.html', error="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return render_template('index.html', error="Server error. Please try again later."), 500
