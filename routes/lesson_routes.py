from flask import Blueprint, render_template, request, abort
from utils.content_loader import load_tracks, load_lesson, load_track_lessons

lesson_bp = Blueprint('lesson', __name__)

@lesson_bp.route('/track/<track_id>')
def track(track_id):
    """Render a specific learning track with its lessons."""
    tracks = load_tracks()
    track = next((t for t in tracks if t['id'] == track_id), None)
    
    if not track:
        abort(404)
        
    lessons = load_track_lessons(track_id)
    return render_template('track.html', track=track, lessons=lessons)

@lesson_bp.route('/lesson/<track_id>/<lesson_id>')
def lesson(track_id, lesson_id):
    """Render a specific lesson with its tutorial content."""
    tracks = load_tracks()
    track = next((t for t in tracks if t['id'] == track_id), None)
    
    if not track:
        abort(404)
        
    lesson_data = load_lesson(track_id, lesson_id)
    
    if not lesson_data:
        abort(404)
        
    return render_template('lesson.html', track=track, lesson=lesson_data)

@lesson_bp.route('/problem/<track_id>/<lesson_id>/<problem_id>')
def problem(track_id, lesson_id, problem_id):
    """Render a specific problem for a lesson."""
    tracks = load_tracks()
    track = next((t for t in tracks if t['id'] == track_id), None)
    
    if not track:
        abort(404)
        
    lesson_data = load_lesson(track_id, lesson_id)
    
    if not lesson_data:
        abort(404)
    
    problem_data = next((p for p in lesson_data.get('problems', []) if p['id'] == problem_id), None)
    
    if not problem_data:
        abort(404)
        
    return render_template('problem.html', track=track, lesson=lesson_data, problem=problem_data)
