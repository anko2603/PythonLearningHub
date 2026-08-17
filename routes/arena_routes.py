from flask import Blueprint, render_template, request, jsonify, abort
from utils.content_loader import load_arena_problems, load_arena_problem
from utils.code_executor import run_arena_test_cases, execute_code

arena_bp = Blueprint('arena', __name__)

@arena_bp.route('/arena')
def arena_index():
    """LeetCode style problem directory."""
    difficulty = request.args.get('difficulty')
    category = request.args.get('category')
    search = request.args.get('search', '').lower()
    
    all_problems = load_arena_problems()
    
    filtered_problems = all_problems
    if difficulty:
        filtered_problems = [p for p in filtered_problems if p.get('difficulty', '').lower() == difficulty.lower()]
    if category:
        filtered_problems = [p for p in filtered_problems if p.get('category', '').lower() == category.lower()]
    if search:
        filtered_problems = [
            p for p in filtered_problems 
            if search in p.get('title', '').lower() 
            or search in p.get('category', '').lower()
            or search in p.get('description', '').lower()
        ]
        
    categories = sorted(list(set(p.get('category', 'General') for p in all_problems)))
    
    stats = {
        'total': len(all_problems),
        'easy': len([p for p in all_problems if p.get('difficulty') == 'Easy']),
        'medium': len([p for p in all_problems if p.get('difficulty') == 'Medium']),
        'hard': len([p for p in all_problems if p.get('difficulty') == 'Hard']),
    }
    
    return render_template(
        'arena.html',
        problems=filtered_problems,
        categories=categories,
        current_difficulty=difficulty,
        current_category=category,
        current_search=search,
        stats=stats
    )

@arena_bp.route('/arena/<problem_id>')
def arena_problem(problem_id):
    """LeetCode split-screen problem solving workspace."""
    problem = load_arena_problem(problem_id)
    if not problem:
        abort(404)
        
    all_problems = load_arena_problems()
    problem_ids = [p['id'] for p in all_problems]
    try:
        curr_idx = problem_ids.index(problem_id)
        prev_id = problem_ids[curr_idx - 1] if curr_idx > 0 else None
        next_id = problem_ids[curr_idx + 1] if curr_idx < len(problem_ids) - 1 else None
    except ValueError:
        prev_id, next_id = None, None
        
    return render_template(
        'arena_problem.html',
        problem=problem,
        prev_id=prev_id,
        next_id=next_id
    )

@arena_bp.route('/api/arena/run', methods=['POST'])
def api_arena_run():
    """Runs code against sample visible test cases."""
    data = request.get_json() or {}
    problem_id = data.get('problem_id')
    user_code = data.get('code', '')
    
    if not problem_id or not user_code:
        return jsonify({'success': False, 'message': 'Missing problem_id or code'}), 400
        
    problem = load_arena_problem(problem_id)
    if not problem:
        return jsonify({'success': False, 'message': 'Problem not found'}), 404
        
    # Run only sample (first 2) test cases for fast preview
    sample_tests = [t for t in problem.get('test_cases', []) if 'Sample' in t.get('name', '')]
    if not sample_tests:
        sample_tests = problem.get('test_cases', [])[:2]
        
    result = run_arena_test_cases(user_code, sample_tests)
    return jsonify(result)

@arena_bp.route('/api/arena/submit', methods=['POST'])
def api_arena_submit():
    """Runs code against complete test suite (both sample and hidden)."""
    data = request.get_json() or {}
    problem_id = data.get('problem_id')
    user_code = data.get('code', '')
    
    if not problem_id or not user_code:
        return jsonify({'success': False, 'message': 'Missing problem_id or code'}), 400
        
    problem = load_arena_problem(problem_id)
    if not problem:
        return jsonify({'success': False, 'message': 'Problem not found'}), 404
        
    all_tests = problem.get('test_cases', [])
    result = run_arena_test_cases(user_code, all_tests)
    return jsonify(result)
