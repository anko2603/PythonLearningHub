from flask import Blueprint, render_template
from utils.content_loader import load_tracks

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Render the homepage with learning tracks."""
    tracks = load_tracks()
    return render_template('index.html', tracks=tracks)
