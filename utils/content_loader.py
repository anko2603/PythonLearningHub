import os
import json
import logging

def load_tracks():
    """Load all learning tracks from the tracks.json file."""
    try:
        with open('content/tracks.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, create it with default tracks
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
        
        os.makedirs('content', exist_ok=True)
        with open('content/tracks.json', 'w') as f:
            json.dump(default_tracks, f, indent=2)
            
        return default_tracks
    except Exception as e:
        logging.error(f"Error loading tracks: {str(e)}")
        return []

def load_track_lessons(track_id):
    """Load all lessons for a specific track."""
    lessons = []
    track_dir = f'content/{track_id}'
    
    try:
        if not os.path.exists(track_dir):
            os.makedirs(track_dir, exist_ok=True)
            return []
            
        for filename in os.listdir(track_dir):
            if filename.endswith('.json'):
                lesson_id = filename[:-5]  # Remove .json extension
                lesson_data = load_lesson(track_id, lesson_id)
                if lesson_data:
                    lessons.append({
                        'id': lesson_id,
                        'title': lesson_data.get('title', 'Untitled'),
                        'description': lesson_data.get('description', ''),
                        'order': lesson_data.get('order', 0)
                    })
        
        # Sort lessons by order
        lessons.sort(key=lambda x: x.get('order', 0))
        return lessons
    except Exception as e:
        logging.error(f"Error loading lessons for track {track_id}: {str(e)}")
        return []

def load_lesson(track_id, lesson_id):
    """Load a specific lesson's content."""
    try:
        lesson_path = f'content/{track_id}/{lesson_id}.json'
        
        if not os.path.exists(lesson_path):
            return None
            
        with open(lesson_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading lesson {lesson_id} in track {track_id}: {str(e)}")
        return None
