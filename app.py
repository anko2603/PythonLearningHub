import os
from flask import Flask

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "python-learning-hub-secret-key-2026")

from routes.main_routes import main_bp
from routes.lesson_routes import lesson_bp
from routes.code_routes import code_bp
from routes.arena_routes import arena_bp
from routes.quiz_routes import quiz_bp
from routes.playground_routes import playground_bp

app.register_blueprint(main_bp)
app.register_blueprint(lesson_bp)
app.register_blueprint(code_bp)
app.register_blueprint(arena_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(playground_bp)
