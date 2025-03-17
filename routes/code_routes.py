import json
from flask import Blueprint, request, jsonify
from utils.code_executor import execute_code, validate_solution

code_bp = Blueprint('code', __name__)

@code_bp.route('/execute', methods=['POST'])
def execute():
    """Execute Python code and return the result."""
    data = request.get_json()
    
    if not data or 'code' not in data:
        return jsonify({'error': 'No code provided'}), 400
    
    code = data['code']
    result = execute_code(code)
    
    return jsonify(result)

@code_bp.route('/validate', methods=['POST'])
def validate():
    """Validate user solution against expected output and tests."""
    data = request.get_json()
    
    if not data or 'code' not in data or 'tests' not in data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    code = data['code']
    tests = data['tests']
    expected_output = data.get('expected_output', None)
    
    result = validate_solution(code, tests, expected_output)
    
    return jsonify(result)
