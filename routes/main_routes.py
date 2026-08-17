from flask import Blueprint, render_template
from utils.content_loader import load_tracks, load_arena_problems, load_quizzes

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Render the ultra-modern homepage with stats, tracks, arena preview, and quiz spotlights."""
    tracks = load_tracks()
    problems = load_arena_problems()[:4]
    quizzes = load_quizzes()[:3]
    
    stats = {
        'total_lessons': 12,
        'total_problems': len(load_arena_problems()),
        'total_quizzes': len(load_quizzes()),
        'active_learners': '10,000+'
    }
    
    return render_template('index.html', tracks=tracks, problems=problems, quizzes=quizzes, stats=stats)
