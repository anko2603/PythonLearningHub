import os
import json
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(BASE_DIR, 'content')

def load_tracks():
    """Load all learning tracks from the tracks.json file."""
    try:
        tracks_file = os.path.join(CONTENT_DIR, 'tracks.json')
        with open(tracks_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        default_tracks = [
            {
                "id": "beginner",
                "title": "Python Basics",
                "description": "Learn the fundamentals of Python programming, from variables to control flow.",
                "icon": "code"
            },
            {
                "id": "intermediate",
                "title": "Intermediate Python",
                "description": "Deepen your Python skills with functions, data structures, and more.",
                "icon": "code-slash"
            },
            {
                "id": "advanced",
                "title": "Advanced Python",
                "description": "Master advanced Python concepts like OOP, decorators, and generators.",
                "icon": "braces"
            }
        ]
        os.makedirs(CONTENT_DIR, exist_ok=True)
        with open(os.path.join(CONTENT_DIR, 'tracks.json'), 'w', encoding='utf-8') as f:
            json.dump(default_tracks, f, indent=2)
        return default_tracks
    except Exception as e:
        logging.error(f"Error loading tracks: {str(e)}")
        return []

def load_track_lessons(track_id):
    """Load all lessons for a specific track."""
    lessons = []
    track_dir = os.path.join(CONTENT_DIR, track_id)
    try:
        if not os.path.exists(track_dir):
            os.makedirs(track_dir, exist_ok=True)
            return []
            
        for filename in os.listdir(track_dir):
            if filename.endswith('.json'):
                lesson_id = filename[:-5]
                lesson_data = load_lesson(track_id, lesson_id)
                if lesson_data:
                    lessons.append({
                        'id': lesson_id,
                        'title': lesson_data.get('title', 'Untitled'),
                        'description': lesson_data.get('description', ''),
                        'order': lesson_data.get('order', 0)
                    })
        lessons.sort(key=lambda x: x.get('order', 0))
        return lessons
    except Exception as e:
        logging.error(f"Error loading lessons for track {track_id}: {str(e)}")
        return []

def load_lesson(track_id, lesson_id):
    """Load a specific lesson's content."""
    try:
        lesson_path = os.path.join(CONTENT_DIR, track_id, f'{lesson_id}.json')
        if not os.path.exists(lesson_path):
            return None
        with open(lesson_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading lesson {lesson_id} in track {track_id}: {str(e)}")
        return None

def load_arena_problems():
    """Load all LeetCode / HackerRank problems from arena_problems.json."""
    try:
        arena_file = os.path.join(CONTENT_DIR, 'arena_problems.json')
        with open(arena_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading arena problems: {str(e)}")
        return []

def load_arena_problem(problem_id):
    """Load a single problem by ID."""
    problems = load_arena_problems()
    return next((p for p in problems if p.get('id') == problem_id), None)

def load_quizzes():
    """Load all interactive quizzes."""
    try:
        quizzes_file = os.path.join(CONTENT_DIR, 'quizzes.json')
        with open(quizzes_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading quizzes: {str(e)}")
        return []

def load_quiz(quiz_id):
    """Load a single quiz by ID."""
    quizzes = load_quizzes()
    return next((q for q in quizzes if q.get('id') == quiz_id), None)
