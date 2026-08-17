from flask import Blueprint, render_template, request, jsonify
from utils.code_executor import execute_code

playground_bp = Blueprint('playground', __name__)

@playground_bp.route('/playground')
def playground():
    """Interactive Python code playground / sandbox."""
    return render_template('playground.html')

@playground_bp.route('/api/playground/run', methods=['POST'])
def run_playground_code():
    data = request.get_json() or {}
    code = data.get('code', '')
    if not code:
        return jsonify({'success': False, 'error': 'No code provided'}), 400
        
    result = execute_code(code)
    return jsonify(result)
