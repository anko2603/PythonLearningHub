from flask import Blueprint, render_template, request, jsonify, abort
from utils.content_loader import load_quizzes, load_quiz

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/quizzes')
def quiz_hub():
    """Gamified Quiz Hub."""
    quizzes = load_quizzes()
    return render_template('quizzes.html', quizzes=quizzes)

@quiz_bp.route('/quiz/<quiz_id>')
def quiz_play(quiz_id):
    """Play a specific interactive quiz."""
    quiz = load_quiz(quiz_id)
    if not quiz:
        abort(404)
    return render_template('quiz_play.html', quiz=quiz)

@quiz_bp.route('/api/quiz/submit', methods=['POST'])
def api_quiz_submit():
    """Evaluate quiz answers, compute streak multiplier, score, and XP."""
    data = request.get_json() or {}
    quiz_id = data.get('quiz_id')
    user_answers = data.get('answers', {})
    
    quiz = load_quiz(quiz_id)
    if not quiz:
        return jsonify({'success': False, 'message': 'Quiz not found'}), 404
        
    questions = quiz.get('questions', [])
    total_q = len(questions)
    correct_count = 0
    detailed_results = []
    
    for q in questions:
        q_id = str(q.get('id'))
        user_choice = user_answers.get(q_id)
        is_correct = (user_choice is not None) and (int(user_choice) == int(q.get('correct_answer')))
        if is_correct:
            correct_count += 1
            
        detailed_results.append({
            'question_id': q.get('id'),
            'user_choice': user_choice,
            'correct_answer': q.get('correct_answer'),
            'is_correct': is_correct,
            'explanation': q.get('explanation', '')
        })
        
    score_percentage = round((correct_count / total_q) * 100, 1) if total_q > 0 else 0
    earned_xp = int(quiz.get('xp', 100) * (score_percentage / 100))
    
    return jsonify({
        'success': True,
        'score_percentage': score_percentage,
        'correct_count': correct_count,
        'total_count': total_q,
        'earned_xp': earned_xp,
        'results': detailed_results
    })
